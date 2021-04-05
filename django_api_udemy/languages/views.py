from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import language_serializer
from .serializer import *
from rest_framework import status
from rest_framework import viewsets
from .models import UserProfile
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from .permissions import updateownprofile
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.settings import api_settings


# Create your views here.
class api_view(APIView):
    serializer_class = language_serializer

    def get(self, request, format=None):
        list = ["hello", "hi"]
        return Response({"list": list})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Added {name}"
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({"PUT": "PUT"})

    def patch(self, request, pk=None):
        return Response({"PATCH": "PATCH"})

    def delete(self, request, pk=None):
        return Response({"DELETED": "Delete"})


class hello_viewset(viewsets.ViewSet):
    serializer_class = language_serializer

    def list(self, request):
        list = ["hello"]
        return Response({"list": list})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"hello {name}"
            return Response({"message": message})
        else:
            return Response(serializer.error,
                            status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        return Response({"method": "update"})

    def partial_update(self, request, pk=None):
        return Response({"method": "partial_update"})

    def retrieve(self, request, pk=None):
        return Response({"method": "retrieve"})

    def destroy(self, request, pk=None):
        return Response({"method": "delete"})


class profile(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfile_serializer
    authentication_classes = (TokenAuthentication,)
    Permission_classes = (updateownprofile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', "email")



