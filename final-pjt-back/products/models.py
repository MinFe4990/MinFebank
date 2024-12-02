from django.db import models
from django.conf import settings

# Create your models here.

class Bank(models.Model): #은행명
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

class JoinDeny(models.Model):# 가입제한
    join_deny = models.CharField(max_length=10)
    # 1: 제한없음 2: 서민전용 3: 일부제한


class Deposit(models.Model): # 예금
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    join_deny = models.ForeignKey(JoinDeny, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250) # 제품코드
    join_way = models.CharField(max_length=250) # 가입방법
    final_init =models.CharField(max_length=250) # 만기 후 이자율
    special_cnd = models.CharField(max_length=250) # 우대조건
    start_day = models.DateField() # 공시 시작일
    end_day = models.DateField(null=True) # 공시 종료일
    max_limit = models.IntegerField(null=True) # 최고 한도
    join_member = models.CharField(max_length=250) # 가입대상

class DepositOption(models.Model): # 예금 옵션
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='options')
    intr_type = models.CharField(max_length=250,null=True) # 저축 금리 유형
    intr_type_name = models.CharField(max_length=250,null=True) # 저축 금리 유형명
    save_term = models.IntegerField() # 저축 기간
    intr_rate = models.FloatField(null=True) # 저축 금리
    intr_rate2 = models.FloatField(null=True) # 최고 우대 금리
    user_change = models.BooleanField(default=False)

class SignedDeposit(models.Model): # 가입한 상품
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)

class SignedDepositOption(models.Model): #가입한 예금 옵션
    signed_deposit = models.ForeignKey(SignedDeposit, on_delete=models.CASCADE)
    deposit_option = models.ForeignKey(DepositOption, on_delete=models.CASCADE)
    

class Saving(models.Model): # 적금옵션
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    join_deny = models.ForeignKey(JoinDeny, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250) # 제품코드
    join_way = models.CharField(max_length=250) # 가입방법
    final_init =models.CharField(max_length=250) # 만기 후 이자율
    special_cnd = models.CharField(max_length=255) # 우대조건
    start_day = models.DateField() # 공시 시작일
    end_day = models.DateField(null=True) # 공시 종료일
    max_limit = models.IntegerField(null=True) # 최고 한도
    join_member = models.CharField(max_length=250) # 가입대상

class SavingOption(models.Model): # 적금 옵션
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, related_name='options')
    intr_type = models.CharField(max_length=250,null=True) # 저축 금리 유형
    intr_type_name = models.CharField(max_length=250,null=True) # 저축 금리 유형명
    save_term = models.IntegerField() # 저축 기간
    intr_rate = models.FloatField(null=True) # 저축 금리
    intr_rate2 = models.FloatField(null=True) # 최고 우대 금리
    rsrv_type = models.CharField(max_length=250,null=True) # 적립 유형 
    rsrv_type_name = models.CharField(max_length=250,null=True) # 적립 유형 이름
    user_change = models.BooleanField(default=False)

class SignedSaving(models.Model): # 가입한 상품
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE)

class SignedSavingOption(models.Model): #가입한 예금 옵션
    signed_saving = models.ForeignKey(SignedSaving, on_delete=models.CASCADE)
    saving_option = models.ForeignKey(SavingOption, on_delete=models.CASCADE)
    
