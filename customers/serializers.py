from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    email = serializers.CharField()

    class Meta:
        model = Customer

        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "address",
            "city",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "full_name",
            "created_at",
            "updated_at",
        ]

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "First name cannot be empty."
            )

        return value.strip()

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Last name cannot be empty."
            )

        return value.strip()

    def validate_email(self, value):
        value = value.strip().lower()

        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError(
                "Only Gmail addresses are allowed."
            )

        return value

    def validate_phone_number(self, value):
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) != 11:
            raise serializers.ValidationError(
                "Phone number must contain 11 digits."
            )

        return value

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"