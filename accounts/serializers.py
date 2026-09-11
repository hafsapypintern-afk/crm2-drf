from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
        ]

        read_only_fields = [
            "id",
            "email",
        ]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "password",
        ]

        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):

        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user