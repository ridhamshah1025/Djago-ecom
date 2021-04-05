from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.core import exceptions


# class add_to_cart_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ("id", "user_id", "product_id", "order_quantity", "is_purchase")

# class User_serializer(serializers.ModelSerializer):
#     # username = serializers.CharField(max_length=255)
#     # password = serializers.CharField(max_length=255)
#
#     def validate(self, data):
#         username = data.get("username")
#         password = data.get("password")
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     data["user"] = user
#                 else:
#                     msg = "user not activated"
#                     raise exceptions.ValidationError(msg)
#         else:
#             msg = "MUST provide email and password"
#             raise exceptions.ValidationError(msg)
#         return data


# class registration_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile

#         fields = ("email", "name", "password")
#         extra_kwargs = {
#             "password": {
#                 'write_only': True,
#                 "style": {"input_type": "password"}
#             }
#
#         }
#
#     def create(self, validated_data):

#         user = UserProfile.objects.create_user(email=validated_data['email'], name=validated_data["name"],
#                                                password=validated_data["password"])
#         # print(user)
#         return user


# class user_data_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ("id", "email", "is_active")
