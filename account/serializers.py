from rest_framework import serializers
from account.models import Account
from account.utils import Utils


class AccountSerializer(serializers.ModelSerializer):
    # account_type = serializers.StringRelatedField(many=False)

    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "account_no", "owner"]
        extra_kwargs = {
            "initial_deposit_date": {"write_only": True},
            "interest_start_date": {"write_only": True},
        }

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

        # # user=user,
        # account_type=validated_data["account_type"],
        # account_no=account_no,
        # balance=validated_data["balance"],
        # interest_start_date=validated_data.get("interest_start_date")
        # if validated_data.get("interest_start_date")
        # else None,
        # initial_deposit_date=validated_data.get("initial_deposit_date")
        # if validated_data.get("initial_deposit_date")
        # else None,
