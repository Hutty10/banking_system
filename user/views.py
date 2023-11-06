from decouple import config
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from user.models import User
from user.serializers import (
    LoginSerializer,
    RegisterSerializer,
    RequestPasswordResetSerializer,
    SetNewPasswordSerializer,
    UserSerializer,
)
from user.utils import CustomRedirect, Utils, activation_token

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        request_body=RegisterSerializer,
    )
    def post(self, request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "User created successful check your email to activate account",
            "data": serializer.data,
            "status": True,
            "status_code": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token) -> Response:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
        if user is not None and activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            response = {
                "message": "Email confirmation successful",
                "data": {},
                "status": True,
                "status_code": status.HTTP_202_ACCEPTED,
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)

        response = {
            "message": "Invalid token",
            "data": {},
            "status": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
        }
        return Response(
            response,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="Login an existing user",
        request_body=LoginSerializer,
    )
    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            "message": "Login successful",
            "data": serializer.data,
            "status": True,
            "status_code": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    @swagger_auto_schema(
        operation_summary="Request password reset",
        request_body=RequestPasswordResetSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get("email", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            print(uidb64)
            token = activation_token.make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                "user:password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
            )

            redirect_url = request.data.get("redirect_url", "")
            absurl = "http://" + current_site + relativeLink
            email_body = f"Hello, \n Use link below to reset your password  \n{absurl}?redirect_url={redirect_url}"
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your passsword",
            }
            Utils.send_email(data)
        response = {
            "message": "We have sent you a link to reset your password",
            "data": {},
            "status": True,
            "status_code": status.HTTP_200_OK,
        }
        return Response(
            response,
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckView(APIView):
    # serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get("redirect_url")
        if not (redirect_url and len(redirect_url) > 3):
            redirect_url = config("FRONTEND_RESET_URL")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
            if not activation_token.check_token(user, token):
                return CustomRedirect(redirect_url + "?token_valid=False")

            return CustomRedirect(
                redirect_url
                + "?token_valid=True&message=Credentials Valid&uidb64="
                + uidb64
                + "&token="
                + token
            )

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not activation_token().check_token(user):
                    return CustomRedirect(redirect_url + "?token_valid=False")

            except UnboundLocalError as e:
                response = {
                    "message": "Token is not valid, please request a new one",
                    "data": {},
                    "status": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }
                return Response(
                    response,
                    status=status.HTTP_400_BAD_REQUEST,
                )


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer

    @swagger_auto_schema(
        operation_summary="Change user password",
        request_body=SetNewPasswordSerializer,
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "message": "Password reset success",
            "data": {},
            "status": True,
            "status_code": status.HTTP_200_OK,
        }
        return Response(
            response,
            status=status.HTTP_200_OK,
        )


class UserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
