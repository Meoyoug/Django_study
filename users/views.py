from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from django.contrib.auth.password_validation import validate_password
from .serializers import MyinfoUserSerializer
#토큰 인증에 관한 라이브러리 가져오기
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import jwt
from users.models import User
from rest_framework_simplejwt import 
# api/v1/users [POST] => 유저 생성 API
class Users(APIView):
    def post(self, request):
        # password => 검증, 해쉬화해서 저장
        # the other => 비밀번호 외 다른 데이터들
        password = request.data.get('password')
        serializer = MyinfoUserSerializer(data=request.data)

        try:
            validate_password(password)
        except:
            return ParseError("Invalid Password")
        
        if serializer.is_valid():
            user = serializer.save() # 새로운 유저를 생성
            user.set_password(password) # 비밀번호 해쉬화
            user.save()

            serializer = MyinfoUserSerializer(user)

            return Response(serializer.data)
        
        else:
            return ParseError(serializer.errors)

#api/v1/users/myinfo [GET,put]
class MyInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = MyinfoUserSerializer(user)

        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = MyinfoUserSerializer(user, data=request.data, partial=True) # partial => 일부 데이터만 넘겨도 되는지 허용여부

        if serializer.is_valid():
            user = serializer.save()
            serializer = MyinfoUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

from django.contrib.auth import authenticate, login
# api/v1/users/login 
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            raise ParseError('username and password are required')
        
        user = authenticate(username=username, password=password)

        if user :
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else :
            return Response(status=status.HTTP_403_FORBIDDEN)

from django.contrib.auth import logout

# api/v1/users/logout
class Logout(APIView):
    permisson_classes = [IsAuthenticated]

    def post(self, request):
        
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            raise ParseError('username and password are required')
        
        user = authenticate(username=username, password=password)

        if user :
            payload = {"id":user.id, "username":user.username}
            token = jwt.encode(
                payload,
                settings.SECRET_KEY, 
                algorithm='HS256'
                )

            return Response({'token': token})
        else :
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class JWTLogout(APIView):
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            raise ParseError('token is required')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = User.objects.get(id=payload['id'])
        logout(user)

        return Response(status=status.HTTP_200_OK)

from config.authentication import JWTAuthentication
class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"id": user.id, "username": user.username})
    
