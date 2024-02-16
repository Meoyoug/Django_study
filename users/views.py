from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from django.contrib.auth.password_validation import validate_password
from .serializers import MyinfoUserSerializer
#토큰 인증에 관한 라이브러리 가져오기
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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


        