from rest_framework.permissions import BasePermission, IsAdminUser

from account.models import Account


class CanTransact(BasePermission):
    def has_permission(self, request, view):
        try:
            user_id = getattr(request.user, "id")
            account = request.data.get("account")
            account = Account.objects.get(account_no=account)
            # import pdb

            # pdb.set_trace()
            return user_id == (account.owner.id or IsAdminUser)

        except Exception as e:
            print(e)
            return False
