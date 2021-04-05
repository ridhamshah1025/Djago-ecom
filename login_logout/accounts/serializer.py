from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import authenticate
from django.core import exceptions


class UserProfile_serializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "user not activated"
                    raise exceptions.ValidationError(msg)
        else:
            msg = "MUST provide email and password"
            raise exceptions.ValidationError(msg)
        return data


class registration_serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        fields = ("email", "name", "password")
        extra_kwargs = {
            "password": {
                'write_only': True,
                "style": {"input_type": "password"}
            }

        }

    def create(self, validated_data):
        print("*********************************************************************************************************************************")
        user = UserProfile.objects.create_user(email=validated_data['email'], name=validated_data["name"],
                                               password=validated_data["password"])
        # print(user)
        return user


class user_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "email", "is_active")
