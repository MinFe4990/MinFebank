from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
# 모델 불러오기

from .models import *

# Serializer 불러오기
from .serializers import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signout(request):
    if request.method == 'POST': 
        user = request.user
        password = request.data.get("password")
        if password.replace(" ","")=="":
            return Response({"detail": "비밀번호를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        if not authenticate(username=user.username, password=password):
            return Response({"detail": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 회원 탈퇴 처리
        user.delete()
        return Response({"detail": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def superuser(request):
    if request.method == 'GET': 
        user = get_user_model().objects.get(username = request.user)
        serializer = GetSuperUser(user)
        return Response(serializer.data, status=status.HTTP_200_OK)