from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [
    path("", views.Users.as_view()), # api/v1/users/
    path("myinfo", views.MyInfo.as_view()), # api/v1/users/myinfo

    # Authentication
    path("getToken", obtain_auth_token), # api/v1/users/getToken
    path("login", views.Login.as_view()), # Django Session login
    path("logout", views.Logout.as_view()), # Django Session logout

    # JWT Authentication
    path("login/jwt", views.JWTLogin.as_view()), # JWT login
    path("logout/jwt", views.JWTLogout.as_view()), # JWT logout
    path("login/jwt/info", views.UserDetailView.as_view()), # JWT login 후 내 정보 확인

    # Simple JWT Authentication
    path("login/simpleJWT", TokenObtainPairView.as_view()), # 최초 로그인시 refresh token, access token 발급
    path("login/simpleJWT/refresh", TokenRefreshView.as_view()), # Refresh token을 body 데이터로 넘겨받아 새로운 access token을 발급
    path("login/simpleJWT/verify", TokenVerifyView.as_view()),  # access token을 body 데이터로 넘겨받아 유효한 토큰인지 확인
]