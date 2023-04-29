from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User

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
