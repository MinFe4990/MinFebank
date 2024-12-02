from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from django.conf import settings
UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # address, address_detail, postcode 추가
    last_name= serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=150
    )
    first_name= serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=150
    )
    address= serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=150
    )
    address_detail= serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=150
    )
    postcode= serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=150
    )

    # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            # nickname 필드 추가
            'address': self.validated_data.get('address', ''),
            'address_detail': self.validated_data.get('address_detail', ''),
            'postcode': self.validated_data.get('postcode', ''),

            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            }
    

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta: # 만일 확인하고 싶은 항목을 바꾸고 싶을때 if문을 건들면됨.
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'address'):
            extra_fields.append('address')
        if hasattr(UserModel, 'address_detail'):
            extra_fields.append('address_detail')
        if hasattr(UserModel, 'postcode'):
            extra_fields.append('postcode')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)
    def validate_username(self, value):
        user = self.context['request'].user
        if value != user.username and UserModel.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value
    

class UserSignoutSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields = ('pk','username','password',)

class GetSuperUser(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields = ('is_superuser',)