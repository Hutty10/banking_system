from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from user.models import User
from user.utils import activation_token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True, required=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "title",
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "phone",
            "password",
        ]
        extra_kwargs = {
            "is_active": {"read_only": True},
            "is_verified": {"read_only": True},
            "password": {"write_only": True},
            "user_permissions": {"read_only": True},
        }

    def validate(self, attrs):
        first_name = attrs.get("first_name", "")
        last_name = attrs.get("last_name", "")

        if not first_name.isalpha():
            raise serializers.ValidationError(
                "first name should only be alphabetic char"
            )
        if not last_name.isalpha():
            raise serializers.ValidationError(
                "last name should only be alphabetic char"
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ["token", "uidb64"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, write_only=True)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])
        return {"access": user.tokens()["access"], "refresh": user.tokens()["refresh"]}

    class Meta:
        model = User
        fields = ["email", "tokens", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = authenticate(email=email, password=password)

        if not user:
            raise exceptions.AuthenticationFailed("Invalid credentials, try again")

        if not user.is_verified:
            raise exceptions.AuthenticationFailed(
                "Email not verified please verify your email"
            )
        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                "Account disabled please contact the admin"
            )

        return {"tokens": user.tokens, "email": user.email}


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=6)
    redirect_url = serializers.CharField(
        max_length=500, required=False, write_only=True
    )

    class Meta:
        fields = ["email", "redirect_url"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not activation_token.check_token(user, token):
                raise exceptions.AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception:
            raise exceptions.AuthenticationFailed("The reset link is invalid", 401)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "is_active",
            "is_verified",
            "created_at",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }
