from rest_framework import serializers
from account.models import Account
from account.utils import Utils


class AccountSerializer(serializers.ModelSerializer):
    # account_type = serializers.SlugRelatedField(slug_field="name", )

    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "account_no"]
        extra_kwargs = {
            "initial_deposit_date": {"write_only": True},
            "interest_start_date": {"write_only": True},
        }

    def create(self, validated_data):
        account_no = Utils.generate_account_no()
        user = self.context.get("user", "")
        unique = False
        while not unique:
            if not Account.objects.filter(account_no=account_no):
                unique = True
            else:
                account_no = Utils.generate_account_no()

        return Account.objects.create(
            user=user,
            account_type=validated_data["account_type"],
            account_no=account_no,
            balance=validated_data["balance"],
            interest_start_date=validated_data["interest_start_date"],
            initial_deposit_date=validated_data["initial_deposit_date"],
        )
