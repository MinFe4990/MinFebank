from django.shortcuts import render
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework import status
import requests
import datetime
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404,get_list_or_404
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# 모델 불러오기
from .models import *

# Serializer 불러오기
from .serializers import *


fin_api_key = settings.FIN_API_KEY

option_name = { 
                'intr_type' : "금리 유형" , 
                'intr_type_name' : "금리 유형 명" ,
                'intr_rate' : "저축 금리" ,
                'intr_rate2' : "최고 우대 금리" ,
                'rsrv_type' : "적립 유형",
                'rsrv_type_name' : "적립 유형명",
            }

def send_email_notification(subject, message, recipient_list, from_email='kmc4889@naver.com'):
    try:
        # 이메일 객체 생성
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list
        )

        # 이메일 전송
        email.send()
        return True
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
        return False



@api_view(['GET'])
def deposit(request):
    if request.method == 'GET':
        url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={fin_api_key}&topFinGrpNo=020000&pageNo=1'
        response= requests.get(url).json()
        denys = {
            1 : '제한없음',
            2 : '서민전용',
            3 : '일부전용'
        }

        for li in response['result'].get('baseList'):
            bank_code = li.get('fin_co_no')
            bank_name = li.get('kor_co_nm')
            product_name = li.get('fin_prdt_nm')
            product_code = li.get('fin_prdt_cd') # 제품코드
            join_way = li.get('join_way') # 가입방법
            final_init = li.get('mtrt_int') # 만기 후 이자율
            special_cnd = li.get('spcl_cnd') # 우대조건
            start_day = li.get('dcls_strt_day') # 공시 시작일
            end_day = li.get('dcls_end_day') # 공시 종료일
            max_limit = li.get('max_limit') # 최고 한도
            join_member = li.get('join_member') # 가입대상
            join_deny = li.get('join_deny') # 가입 제한대상

            if not Bank.objects.filter(code=bank_code).exists():
                bank = Bank.objects.create(name=bank_name,code=bank_code)
                bank.save()

            if not JoinDeny.objects.filter(pk=join_deny).exists():
                joinDeny = JoinDeny.objects.create(pk=join_deny,join_deny=denys[int(join_deny)])
                joinDeny.save()

            if start_day!=None:
                start_day = datetime.strptime(start_day,'%Y%m%d').date()
            if end_day!=None:
                end_day = datetime.strptime(end_day,'%Y%m%d').date()
            savedata = {
                'name' : product_name,
                'code' : product_code,
                'join_way':join_way,
                'final_init':final_init,
                'special_cnd':special_cnd,
                'start_day':start_day,
                'end_day':end_day,
                'max_limit':max_limit,
                'join_member':join_member,
            }

            if Deposit.objects.filter(code = product_code,).exists():
            #     이미 있는 제품일 경우 변동사항 확인
                if not Deposit.objects.filter(**savedata).exists():
                    deposit = Deposit.objects.get(code = product_code)
                    serializer = DepositSerializer(
                        deposit,
                        data = savedata,
                        partial=True,
                    )
                    if serializer.is_valid():
                        serializer.save()
                continue


            bank = get_object_or_404(Bank,code=bank_code)
            joinDeny = get_object_or_404(JoinDeny,pk=join_deny)


            serializers = DepositSerializer(data=savedata)
            if serializers.is_valid(raise_exception=True):
                serializers.save(bank= bank,join_deny=joinDeny)

        for li in response['result'].get('optionList'):

            deposit_code = li.get('fin_prdt_cd')
            intr_type = li.get('intr_rate_type')
            intr_type_name = li.get('intr_rate_type_nm')

            save_term = li.get('save_trm')
            intr_rate = li.get('intr_rate')
            intr_rate2 = li.get('intr_rate2')

            savedata = {
                'intr_type' : intr_type,
                'intr_type_name' : intr_type_name,
                'save_term':save_term,
                'intr_rate':intr_rate,
                'intr_rate2':intr_rate2,
            }

            deposit = get_object_or_404(Deposit,code=deposit_code)
            if DepositOption.objects.filter(deposit=deposit.id,save_term=save_term).exists():
                query = {"deposit":deposit.id}
                query.update(savedata)
                if not DepositOption.objects.filter(**query).exists() and not DepositOption.objects.filter(deposit=deposit.id,save_term=save_term,user_change=True).exists():
                    depositOption = DepositOption.objects.get(deposit=deposit.id,save_term=save_term)
                    serializer = DepositOptionSerializer(
                        depositOption,
                        data = savedata,
                        partial=True,
                    )
                    if serializer.is_valid():
                        serializer.save()
                continue

            savedata["user_change"]=False
            serializers = DepositOptionSerializer(data=savedata)
            if serializers.is_valid(raise_exception=True):
                serializers.save(deposit=deposit)
    deposit = get_list_or_404(Deposit)
    serializers = DepositListSerializer(deposit,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)



@api_view(['GET'])
def saving(request):
    if request.method == 'GET':
        url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={fin_api_key}&topFinGrpNo=020000&pageNo=1'
        response= requests.get(url).json()
        denys = {
            1 : '제한없음',
            2 : '서민전용',
            3 : '일부전용'
        }

        for li in response['result'].get('baseList'):
            bank_code = li.get('fin_co_no')
            bank_name = li.get('kor_co_nm')
            product_name = li.get('fin_prdt_nm')
            product_code = li.get('fin_prdt_cd') # 제품코드
            join_way = li.get('join_way') # 가입방법
            final_init = li.get('mtrt_int') # 만기 후 이자율
            special_cnd = li.get('spcl_cnd') # 우대조건
            start_day = li.get('dcls_strt_day') # 공시 시작일
            end_day = li.get('dcls_end_day') # 공시 종료일
            max_limit = li.get('max_limit') # 최고 한도
            join_member = li.get('join_member') # 가입대상
            join_deny = li.get('join_deny') # 가입 제한대상         

            if not Bank.objects.filter(code=bank_code).exists():
                bank = Bank.objects.create(name=bank_name,code=bank_code)
                bank.save()

            if not JoinDeny.objects.filter(pk=join_deny).exists():
                joinDeny = JoinDeny.objects.create(pk=join_deny,join_deny=denys[int(join_deny)])
                joinDeny.save()

            if start_day!=None:
                start_day = datetime.strptime(start_day,'%Y%m%d').date()
            if end_day!=None:
                end_day = datetime.strptime(end_day,'%Y%m%d').date()
            savedata = {
                'name' : product_name,
                'code' : product_code,
                'join_way':join_way,
                'final_init':final_init,
                'special_cnd':special_cnd,
                'start_day':start_day,
                'end_day':end_day,
                'max_limit':max_limit,
                'join_member':join_member,
            }

            if Saving.objects.filter(code = product_code,).exists(): 
                if not Saving.objects.filter(**savedata,).exists():
                    saving = Saving.objects.get(code = product_code)
                    serializer = SavingSerializer(
                        saving,
                        data = savedata,
                        partial=True,
                    )
                    if serializer.is_valid():
                        serializer.save()
                continue
                
            bank = get_object_or_404(Bank,code=bank_code)
            joinDeny = get_object_or_404(JoinDeny,pk=join_deny)

            serializers = SavingSerializer(data=savedata)
            if serializers.is_valid(raise_exception=True):
                serializers.save(bank= bank,join_deny=joinDeny)

        for li in response['result'].get('optionList'):

            saving_code = li.get('fin_prdt_cd')
            intr_type = li.get('intr_rate_type')
            intr_type_name = li.get('intr_rate_type_nm')
            save_term = li.get('save_trm')
            intr_rate = li.get('intr_rate')
            intr_rate2 = li.get('intr_rate2')
            rsrv_type = li.get('rsrv_type') # 적립 유형 
            rsrv_type_name = li.get('rsrv_type_nm') # 적립 유형 이름

            savedata = {
                'intr_type' : intr_type,
                'intr_type_name' : intr_type_name,
                'save_term':save_term,
                'intr_rate':intr_rate,
                'intr_rate2':intr_rate2,
                'rsrv_type':rsrv_type,
                'rsrv_type_name':rsrv_type_name,
            }

            saving = Saving.objects.get(code=saving_code)
            if SavingOption.objects.filter(saving=saving.id,save_term=save_term).exists():# 아이디와 저장 기간이 있으면 바꾸든가 넘어가던가 해야한다.
                query = {"saving":saving.id}
                query.update(savedata)
                if not SavingOption.objects.filter(**query).exists() and not SavingOption.objects.filter(saving=saving.id,save_term=save_term,user_change=True).exists() : # 완전히 같으면 pass 조금 다르면 변화
                    savingOption = SavingOption.objects.get(saving = saving.id,save_term=save_term)
                    serializer = SavingOptionSerializer(
                        savingOption,
                        data = savedata,
                        partial=True,
                    )
                    if serializer.is_valid():
                        serializer.save()
                continue

            savedata["user_change"]=False
            serializers = SavingOptionSerializer(data=savedata)
            if serializers.is_valid(raise_exception=True):
                serializers.save(saving=saving)
    saving = get_list_or_404(Saving)
    serializers = SavingListSerializer(saving,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def banklist(request):
    if request.method == "GET":
        bank = get_list_or_404(Bank)
        serializers = BankSerializer(bank,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
@api_view(['GET','POST'])
def sign(request):
    user = request.user
    if request.method == "GET":
        # 현재 로그인한 사용자의 SignedSavingOption 데이터 가져오기
        # 쿼리셋 직렬화
        serializers = UserSignedProductSerializer(user)

        return Response(
            serializers.data,
            status=status.HTTP_200_OK
            )
    

    if request.method == "POST":
        product_type = request.data.get('products')
        product_code = request.data.get('prdt_cd')
        option_term = request.data.get('save_term')

        # Saving 상품 처리
        if product_type == 'saving':
            try:
                saving = get_object_or_404(Saving,code=product_code)
                saving_option = get_object_or_404(SavingOption,saving=saving, save_term=option_term)

                # SignedSaving 및 SignedSavingOption 생성

                if SignedSaving.objects.filter(user=user,saving = saving).exists():
                    return Response({"error": "Saving product already Signed"}, status=status.HTTP_404_NOT_FOUND)
                signed_saving = SignedSaving.objects.create(user=user, saving=saving)
                SignedSavingOption.objects.create(signed_saving=signed_saving, saving_option=saving_option)


                
                serializers = UserSignedProductSerializer(user)
                return Response(
                    serializers.data,
                    status=status.HTTP_201_CREATED
                )
            except Saving.DoesNotExist:
                return Response({"error": "Saving product not found"}, status=status.HTTP_404_NOT_FOUND)
            except SavingOption.DoesNotExist:
                return Response({"error": "Saving option not found"}, status=status.HTTP_404_NOT_FOUND)
        elif product_type == 'deposit':
            try:
                deposit = get_object_or_404(Deposit,code=product_code)
                deposit_option = get_object_or_404(DepositOption,deposit=deposit, save_term=option_term)

                # SignedDeposit 및 SignedDepositOption 생성
                if SignedDeposit.objects.filter(user=user,deposit = deposit).exists():
                    return Response({"error": "Deposit product already Signed"}, status=status.HTTP_404_NOT_FOUND)
                signed_deposit = SignedDeposit.objects.create(user=user, deposit=deposit)
                SignedDepositOption.objects.create(signed_deposit=signed_deposit, deposit_option=deposit_option)

                serializers = UserSignedProductSerializer(user)
                return Response(
                    serializers.data,
                    status=status.HTTP_201_CREATED
                )
            except Deposit.DoesNotExist:
                return Response({"error": "Deposit product not found"}, status=status.HTTP_404_NOT_FOUND)
            except DepositOption.DoesNotExist:
                return Response({"error": "Deposit option not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Invalid product type"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def changeOption(request):
    # pk 바꾸고 싶은 옵션 pk
    # products 바꾸고 싶은것 deposit or saving
    code = request.data.get("code")

    save_term = request.data.get("save_term")
    if request.data.get("products")=="deposit":
        deposit = get_object_or_404(Deposit,code=code)
        Options = DepositOption.objects.filter(deposit_id=deposit.pk, save_term = save_term)
    else :
        saving = get_object_or_404(Saving,code = code)
        Options = SavingOption.objects.filter(saving_id=saving.pk,save_term = save_term)

    if Options.exists(): # 옵션이 있다 수정
        if request.data.get("products")=="deposit": # 옵션 수정
            title = "예금 "+deposit.code+"의 변경 내용을 안내드립니다."
            message = ""

            Option = get_object_or_404(DepositOption,deposit_id=deposit.pk, save_term = save_term)
            email = SignedDepositUserEmailsSerializer({'deposit': deposit})
            option_list = { 
            'intr_type' , 
            'intr_type_name' ,
            'intr_rate' ,
            'intr_rate2' ,
            }

            save_data = {
            }

            for option in option_list:
                if request.data.get(option) != None:
                    message+=option_name[option]+" : " + str(getattr(Option, option))+"에서 " + str(request.data.get(option))+"로\n"
                    save_data[option]=request.data.get(option)

            query = {"deposit_id":deposit.pk,"save_term" : save_term} 
            query.update(save_data)
            if DepositOption.objects.filter(**query).exists():
                return Response({'error': "변동사항이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
            save_data["user_change"]=True
            serializer = ChangeDepositOptionSerializer(
                Option,
                data = save_data,
                partial=True,
            )

        else :
            Option = get_object_or_404(SavingOption,saving_id=saving.pk,save_term = save_term)
            email = SignedSavingUserEmailsSerializer({'saving':saving})
            title = "적금 "+saving.code+"의 변경 내용을 안내드립니다."
            message = ""
            option_list = { 
                'intr_type' , 
                'intr_type_name' ,
                'intr_rate' ,
                'intr_rate2' ,
                'rsrv_type',
                'rsrv_type_name',
            }
            
            save_data = {
            }
            for option in option_list:
                if request.data.get(option) != None:
                    message+=option_name[option]+" : " + str(getattr(Option, option))+"에서 " + str(request.data.get(option))+"로\n"
                    save_data[option]=request.data.get(option)
            query = {"saving_id":saving.pk,"save_term" : save_term} 
            query.update(save_data)
            if SavingOption.objects.filter(**query).exists():
                return Response({'error': "변동사항이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
            save_data["user_change"]=True
            
            serializer = ChangeSavingOptionSerializer(
                Option,
                data = save_data,
                partial=True,
            )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message+="로 변동되었음을 알려드립니다."
            send_email_notification(title,message,email.data['user_emails'])
            return Response(serializer.data,status=status.HTTP_200_OK)
            

    else: # 옵션이 없다? 생성해야한다.
        if request.data.get("products")=="deposit": # 옵션 수정
            message=""
            email = SignedDepositUserEmailsSerializer({'deposit': deposit})
            title = "예금 "+deposit.code+"의 생성 내용을 안내드립니다."
            option_list = { 
            'intr_type' , 
            'intr_type_name' ,
            'intr_rate' ,
            'intr_rate2' ,
            }
            save_data = {
                'save_term' : save_term,
            }
            for option in option_list:
                message+=option_name[option]+" : " +  str(request.data.get(option,"None"))+"로 생성되었습니다.\n"
                save_data[option]=request.data.get(option)
            save_data["user_change"]=True
            serializer = DepositOptionSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit=deposit)
                send_email_notification(title,message,email.data['user_emails'])
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        else :
            message=""
            email = SignedSavingUserEmailsSerializer({'saving':saving})
            title = "적금 "+saving.code+"의 생성 내용을 안내드립니다."
            option_list = { 
                'intr_type' , 
                'intr_type_name' ,
                'intr_rate' ,
                'intr_rate2' ,
                'rsrv_type',
                'rsrv_type_name',
            }
            save_data = {
                'save_term' : save_term,
            }
            for option in option_list:
                message+=option_name[option]+" : " + str(request.data.get(option,"None"))+"로 생성되었습니다.\n"
                save_data[option]=request.data.get(option)
            serializer = SavingOptionSerializer(data = save_data)
            save_data["user_change"]=True
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving=saving)
                send_email_notification(title,message,email.data['user_emails'])
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            