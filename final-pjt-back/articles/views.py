from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404,get_list_or_404

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from .models import *
from .serializers import *


@api_view(['GET','POST']) 
def articleControl(request): # article list 조회 및 article 생성
    if request.method == "GET":
        articletype = request.GET.get('type')
        type = get_object_or_404(ArticleType,articletype = articletype)
        serializer = ArticleListSerializer(type)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method == "POST":
        user = request.user # 요청을 보내주는 user
        article_type = request.data.get('type') # ex ) 자유 게시판
        title = request.data.get('title') # 작성한 제목
        content = request.data.get('content') # 작성한 내용
        savedata = {
            'title' : title,
            'content' : content
        }
        serializer = ArticleSerializer(data=savedata)
        if serializer.is_valid(raise_exception=True):
            type = get_object_or_404(ArticleType,articletype=article_type)
            serializer.save(user=user,article_type=type)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def articledetail(request):
    if request.method == "GET": #pk만 받아오면 보여준다.
        article_pk = request.GET.get('article_pk')
        article = get_object_or_404(Article,pk=article_pk)
        # article + 댓글을 가져온다
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == "PUT": # title, content, article_pk를 받아오면 이를 이용해 수정한다. 작성자가 같아야한다.
        article_pk = request.data.get('article_pk')
        article = get_object_or_404(Article,pk=article_pk)
        user = request.user
        title = request.data.get('title')
        content = request.data.get('content')
        savedata = {}
        if user != article.user:
            return Response({'error' : "작성자가 아닙니다."},status=status.HTTP_400_BAD_REQUEST)
        if (title !="" or title!=None) and (content !=""or content!=None):
            savedata['title']=title
            savedata['content']=content
        elif (content !=""or content!=None):
            savedata['content']=content
        elif (title !="" or title!=None):
            savedata['title']=title
        else:
            return Response({'error':'수정데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleSerializer(
            article, data=savedata, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE': # 작성자가 맞으면 삭제한다.
        article_pk = request.data.get('article_pk')
        article = get_object_or_404(Article,pk=article_pk)
        user = request.user
        if user != article.user:
            return Response({'error' : "작성자가 아닙니다."},status=status.HTTP_400_BAD_REQUEST)
        
        article.delete()
        return Response({'message':'데이터가 삭제되었습니다.'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST','PUT','DELETE'])
def commit(request): # commit 추가, commit 수정, commit 삭제 
    # 최소 받아야 할 것 어떤 article에서 작성했는지 article_pk
    if request.method == "GET":
        article_pk = request.GET.get('article_pk')
        article = get_object_or_404(Article,pk=article_pk)
        serializer = CommitListSerializer(article)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "POST": #pk만 받아오면 보여준다.
        article_pk = request.data.get('article_pk')
        article = get_object_or_404(Article,pk=article_pk)

        user = request.user
        content = request.data.get('content')
        savedata = {
            'content': content
        }
        serializer = CommitSerializer(data=savedata)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user,article=article)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    elif request.method == "PUT":
        user = request.user
        content = request.data.get('content')
        commit_pk = request.data.get('commit_pk')
        commit = get_object_or_404(Commit,pk=commit_pk)
        savedata = {}

        if (content !="" or content!=None):
            savedata['content']=content
        else:
            return Response({'error':'수정데이터가 없습니다.'},status=status.HTTP_400_BAD_REQUEST)

        serializer = CommitSerializer(
            commit, data=savedata, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        user = request.user
        content = request.data.get('content')
        user = request.user
        commit_pk = request.data.get('commit_pk')
        commit = get_object_or_404(Commit,pk=commit_pk)
        commit.delete()
        return Response({'message':'데이터가 삭제되었습니다.'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def articleLike(request):
    if request.method =="GET":
        article_pk = request.GET.get("article_pk")
        article = get_object_or_404(Article,pk=article_pk)
        serializer = ArticleLikeUserListSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "POST" :
        # 좋아요 추가 및 삭제
        article_pk = request.data.get('article_pk')
        article = get_object_or_404(Article,pk=article_pk)

        if ArticleLike.objects.filter(user=request.user,article=article).exists():
            articlelike = get_object_or_404(ArticleLike,user=request.user,article=article)
            articlelike.delete()
            return Response({"data": "삭제 완료"}, status=status.HTTP_204_NO_CONTENT)

        else:
            articlelike = ArticleLike.objects.create(user=request.user,article=article)
            articlelike.save()
            return Response({"data": '생성 완료'}, status=status.HTTP_201_CREATED)
        
