from rest_framework import generics, permissions, status
from rest_framework.response import Response

from account.models import Account
from account.serializers import AccountSerializer
from account.utils import Utils
from .permissions import IsOwnerOrAdmin

# Create your views here.


class AccountCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        account_no = Utils.generate_account_no()
        unique = False
        # import pdb

        # pdb.set_trace()
        while not unique:
            if not Account.objects.filter(account_no=account_no):
                unique = True
            else:
                account_no = Utils.generate_account_no()
        serializer.save(owner=request.user, account_no=account_no)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetailView(generics.RetrieveDestroyAPIView):
    lookup_field = "account_no"
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerOrAdmin]
