from rest_framework import serializers
from .models import UserProfile


class language_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)


class UserProfile_serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "name", "email","dob", "password")
        extra_kwargs = {
            "password": {
                'write_only': True,
                "style": {"input_type": "password"}
            }

        }

    def create(self, validated_data):
        user = UserProfile.objects.create_user(email=validated_data['email'], name=validated_data["name"],
                                               dob=validated_data["dob"], password=validated_data["password"])
        return user
