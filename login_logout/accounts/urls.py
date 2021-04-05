from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("view" ,user_data)
urlpatterns = [
    path("",include(router.urls)),
    path("hello", hello_api_view),
    path("check", check_token.as_view()),
    path("login", login_api.as_view()),
    path("logout", logout_api.as_view()),
    path("registration", registration_api.as_view()),

]