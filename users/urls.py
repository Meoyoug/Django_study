from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
urlpatterns = [
    path("", views.Users.as_view()), # api/v1/users/
    path("myinfo", views.MyInfo.as_view()), # api/v1/users/myinfo
    path("getToken", obtain_auth_token), # api/v1/users/getToken
]