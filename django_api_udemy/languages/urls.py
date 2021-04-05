from django.urls import path, include

from .views import hello_viewset
from .views import profile
from .views import api_view
from rest_framework import routers
from rest_framework.authtoken import views
router = routers.DefaultRouter()
router.register("viewset", hello_viewset, basename="viewset")
router.register("profile",profile)
urlpatterns = [

    # path("login/", views.obtain_auth_token),
    path('apiview/', api_view.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('', include(router.urls)),

]