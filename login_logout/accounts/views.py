from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework import permissions
from .serializer import *
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
@decorators.api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def hello_api_view(request):
    return Response({"message": "Hello"})


# @decorators.api_view(["POST"])
# @permission_classes((permissions.AllowAny,))
# def login(request):
#
#     return Response({"message": "Hello"})


class login_api(APIView):
    def post(self, request):
        serializer = UserProfile_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class logout_api(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=204)


class registration_api(APIView):
    def post(self, request):
        serializer = registration_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("before save")
        # data = serializer.validated_data
        # print(data)
        serializer.save()
        print("after save")
        return Response({"user": serializer.data})


class check_token(APIView):
    authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request):
        return Response({"msg": "check"}, template_name="templates/accounts/home.html")


class user_data(viewsets.ModelViewSet):
    serializer_class = user_data_serializer
    queryset = UserProfile.objects.all()
