from rest_framework import generics, status
from rest_framework.response import Response
from account.models import Account
from account.serializers import AccountSerializer
from utils.permissions import IsOwnerOrAdmin

# Create your views here.


class AccountView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetailView(generics.RetrieveDestroyAPIView):
    lookup_field = "pk"
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerOrAdmin]
