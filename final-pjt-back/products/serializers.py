from rest_framework import serializers
from .models import Bank ,Deposit,DepositOption,SignedDeposit,SignedDepositOption,JoinDeny,Saving,SavingOption,SignedSaving,SignedSavingOption
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        exclude = ('id',) 


class JoinDenySerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinDeny
        exclude = ('id',) 

## 예금 옵션
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        exclude = ('id',) 
        read_only_fields = ('bank','join_deny')

class DepositOptionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = DepositOption
        exclude = ('id',) 
        read_only_fields = ('deposit',)

class DepositListSerializer(serializers.ModelSerializer): ## 리스트 전체 불러오기 용
    bank = BankSerializer()
    join_deny = JoinDenySerializer()
    options = DepositOptionSerializer(many=True)  # DepositOption 역참조

    class Meta:
        model = Deposit
        exclude = ('id',) 

#######################################################################################################################

## Saving 예금

class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        exclude = ('id',) 
        read_only_fields = ('bank','join_deny')

class SavingOptionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = SavingOption
        exclude = ('id',) 
        read_only_fields = ('saving',)

class SavingListSerializer(serializers.ModelSerializer): ## 리스트 전체 불러오기 용
    bank = BankSerializer()
    join_deny = JoinDenySerializer()
    options = SavingOptionSerializer(many=True)  # SavingOption 역참조

    class Meta:
        model = Saving
        exclude = ('id',) 


############### User와 연동해서 사용하기용################

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
class SignedSavingOptionSerializer(serializers.ModelSerializer):
    saving_option = SavingOptionSerializer()
    class Meta:
        model = SignedSavingOption
        fields = ['id', 'saving_option']


class SignedSavingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    saving = SavingSerializer()
    options = SignedSavingOptionSerializer(source='signedsavingoption_set', many=True, read_only=True)

    class Meta:
        model = SignedSaving
        fields = ['id', 'user', 'saving', 'options']


class SignedDepositOptionSerializer(serializers.ModelSerializer): #가입한 예적금 옵션
    deposit_option = DepositOptionSerializer()
    class Meta:
        model = SignedDepositOption
        fields = ['id', 'deposit_option']

class SignedDepositSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    deposit = DepositSerializer()
    options = SignedDepositOptionSerializer(source='signeddepositoption_set', many=True, read_only=True)
    class Meta:
        model = SignedDeposit
        fields = ['id', 'user', 'deposit', 'options']

class ChangeDepositOptionSerializer(serializers.ModelSerializer):
    deposit = serializers.CharField(source = 'deposit_set', read_only=True)
    class Meta:
        model = DepositOption
        fields = "__all__"

class ChangeSavingOptionSerializer(serializers.ModelSerializer):
    saving = serializers.CharField(source = 'saving_set', read_only=True)
    class Meta:
        model = SavingOption
        fields = "__all__"






############################################### 가져오기 전용으로 수정



class UserSignedProductSerializer(serializers.ModelSerializer):
    class UserSignedSavingSerializer(serializers.ModelSerializer):
        class UserSignedSavingOptionSerializer(serializers.ModelSerializer):
            saving_option = SavingOptionSerializer()
            class Meta:
                model = SignedSavingOption
                fields = ['saving_option']
                
        saving = SavingSerializer()
        options = UserSignedSavingOptionSerializer(source='signedsavingoption_set', many=True, read_only=True)
        class Meta:
            model = SignedSaving
            fields = ['saving', 'options']

    class UserSignedDepositSerializer(serializers.ModelSerializer):
        class UserSignedDepositOptionSerializer(serializers.ModelSerializer): #가입한 예적금 옵션
            deposit_option = DepositOptionSerializer()
            class Meta:
                model = SignedDepositOption
                fields = ['id', 'deposit_option']
        deposit = DepositSerializer()
        options = UserSignedDepositOptionSerializer(source='signeddepositoption_set', many=True, read_only=True)
        class Meta:
            model = SignedDeposit
            fields = ['deposit', 'options']

    signed_deposit = UserSignedDepositSerializer(source='signeddeposit_set', many=True, read_only=True)
    signed_saving = UserSignedSavingSerializer(source='signedsaving_set', many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username','signed_deposit','signed_saving']

class SignedDepositUserEmailsSerializer(serializers.ModelSerializer):
    user_emails = serializers.SerializerMethodField()
    User = get_user_model()
    class Meta:
        model = SignedDeposit
        fields = ['deposit', 'user_emails']  # 반환할 필드 지정

    def get_user_emails(self, obj):
        # 특정 deposit에 가입한 유저 이메일 리스트 반환
        users = SignedDeposit.objects.filter(deposit=obj['deposit']).select_related('user')
        return [user.user.email for user in users]

class SignedSavingUserEmailsSerializer(serializers.ModelSerializer):
    user_emails = serializers.SerializerMethodField()
    User = get_user_model()
    class Meta:
        model = SignedSaving
        fields = ['saving', 'user_emails']  # 반환할 필드 지정

    def get_user_emails(self, obj):
        # 특정 deposit에 가입한 유저 이메일 리스트 반환
        users = SignedSaving.objects.filter(saving=obj["saving"]).select_related('user')
        return [user.user.email for user in users]