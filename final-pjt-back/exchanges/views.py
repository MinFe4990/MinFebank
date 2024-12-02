from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
import requests
import certifi
from datetime import date , timedelta, datetime
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import status
EX_API_KEY = settings.EX_API_KEY

# 모델 불러오기
from .models import Date, Country, Exchange

# Serializer 불러오기
from .serializers import DateSerializer, CountrySerializer, ExchangeSerializer,ExchangeListSerializer

# Create your views here.


countrysname={
    '유로':"유럽",
    "위안화": '중국',
} # 

@api_view(['GET'])
def exchangelist(request):
    if request.method == 'GET':
        # 범위 내의 데이터에 삭제를 먼저 진행하고 데이터를 받아오면 데이터의 사용량을 줄일 수 있을 것이다.
        day_range = request.GET.get('range') 
        if day_range == "" or day_range == None:
            day_range = 8
        else :
            day_range = int(day_range)

        datalist = {(date.today()-timedelta(days=day)) for day in range(30)}
        dates = Date.objects.all()

        for dater in dates:
            if dater.date not in datalist:
                dater.delete()
        
        startday = date.today()-(timedelta(days=1) if datetime.today().hour<11 else timedelta(days=0) ) # 어제부터 일주일 전 데이터 획득을 위한 어제 설정
        for delta in range(day_range):

            day = startday-timedelta(days=delta) # 7일의 데이터를 받기 위해 for문을 돌린다.
            if not Date.objects.filter(date=day).exists(): # date를 기준으로 모두 받고 date가 없으면 api를 통해 값을 받아온다.[날짜를 통한 데이터 관리]
                fday = day.strftime('%Y%m%d')
                url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={EX_API_KEY}&searchdate={fday}&data=AP01' 
                response= requests.get(url, verify=False).json()
                date_=DateSerializer(data={'date':day})
                if date_.is_valid(raise_exception=True):
                    date_.save() # 없는 날짜니 저장한다.
                
                for li in response:
                    if len(li.get("cur_nm").split())==1: # 위엔화, 유로는 나라가 적혀있지 않아 따로 countrysname dictd을 만들어 이름을 작성
                        country_currency = li.get("cur_nm").split()[0]
                        country_name = countrysname[country_currency]
                    else: # 그 외에는 이름과 통화명이 같이 있다.
                        if "달러"==li.get("cur_nm").split()[1] and "미국"!=li.get("cur_nm").split()[0]: # 통화 이름이 달러일 경우
                            country_currency = li.get("cur_nm") 
                        else:
                            country_currency = li.get("cur_nm").split()[1]
                        country_name = li.get("cur_nm").split()[0]

                    country_code = li.get('cur_unit')
                    exchange_buy = float(li.get('ttb').replace(",","")) # 1000 단위마다 ,이 있어 이를 제거해준다.
                    exchange_sell = float(li.get('tts').replace(",",""))  # 1000 단위마다 ,이 있어 이를 제거해준다.
                

                    if not Country.objects.filter(name=country_name).exists(): # 도시도 중복되므로 해당 도시가 없으면 이름, 코드, 통화를 db에 저장해준다.
                        country = Country.objects.create(
                            name=country_name,
                            code=country_code,
                            currency=country_currency
                            )
                        country.save
                    
                    save_Inf={
                        'buy':exchange_buy,
                        'sell': exchange_sell
                    }
                    

                    country = get_object_or_404(Country,code=country_code)
                    date_ = get_object_or_404(Date,date= day)
                    serializer = ExchangeSerializer(data=save_Inf)

                    if serializer.is_valid(raise_exception=True):
                        serializer.save(country=country,date=date_)
                    # serializer를 이용해 저장

        exchange = get_list_or_404(Exchange)
        serializers = ExchangeListSerializer(exchange,many=True) # 나라 이름과 날짜를 한번에 받을 수 있도록 작성 후 받는다.
        if datetime.today().hour<11:
            return Response({'data':serializers.data,'message':'당일 11시 이전에는 환율이 업데이트 안됩니다.'},status=status.HTTP_200_OK)    
        else: 
            return Response({'data':serializers.data,'message':'당일 환율이 업데이트 되었습니다.'},status=status.HTTP_200_OK)   

@api_view(['GET'])
def country(request):
    if request.method == 'GET':
        country = get_list_or_404(Country)
        serializer = CountrySerializer(country, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)