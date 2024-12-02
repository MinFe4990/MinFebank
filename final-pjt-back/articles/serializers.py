from rest_framework import serializers
from .models import ArticleType,Article,ArticleLike,Commit
from django.contrib.auth import get_user_model


# 기본 저장용 field
class ArticleTypeSerializer(serializers.ModelSerializer): #기본 ArticleType
    class Meta:
        model = ArticleType
        fields = "__all__"
class ArticleSerializer(serializers.ModelSerializer): #기본 Article 가져오기
    article_type = serializers.CharField(source='article_type.name', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Article
        fields = "__all__"
class ArticleLikeSerializer(serializers.ModelSerializer): #기본 Article좋아요 가져오기
    class Meta:
        model = ArticleLike
        fields = "__all__"
        read_only_fields = ('user','article')
class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = "__all__"
        read_only_fields = ('user','article')

# 일기 용 필드
class ArticleReadSerializer(serializers.ModelSerializer):
        articlelike = serializers.IntegerField(source = 'articlelike_set.count',read_only=True)
        user = serializers.CharField(source = 'user.username',read_only=True)
        commitcount = serializers.IntegerField(source = 'commit_set.count',read_only=True)
        class Meta:
            model = Article
            fields = "__all__"



class ArticleListSerializer(serializers.ModelSerializer): # 타입을 받으면 타입에 맞는 모든 Arcticle 조회
    article = ArticleReadSerializer(source = 'article_set',many=True,read_only=True)
    class Meta:
        model = ArticleType
        fields = ('article',)

class CommitReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username',read_only=True)
    class Meta:
        model = Commit
        fields = ['id', 'content', 'user',  'create_at', 'update_at'] 
class ArticleLikeSerializer(serializers.ModelSerializer): #기본 Article좋아요 가져오기
    class Meta:
        model = ArticleLike
        fields = "__all__"
        read_only_fields = ('user','article')

class ArticleDetailSerializer(serializers.ModelSerializer): # 타입을 받으면 타입에 맞는 모든 Arcticle 조회
    articlelike = serializers.IntegerField(source = 'articlelike_set.count',read_only=True)
    likeuser = ArticleLikeSerializer(source='articlelike_set', many=True, read_only=True)
    commit = CommitReadSerializer(source = 'commit_set',read_only=True,many = True)
    user = serializers.CharField(source = 'user.username',read_only=True)
    class Meta:
        model = Article
        fields = ('id','user','title','content','create_at','update_at','articlelike','commit','likeuser')

class ArticleCommitSerializer(serializers.ModelSerializer): # 타입을 받으면 타입에 맞는 모든 Arcticle 조회
    articlelike = serializers.IntegerField(source = 'articlelike_set.count',read_only=True)
    commit = CommitReadSerializer(source = 'commit_set',read_only=True,many = True)
    user = serializers.CharField(source = 'user.username',read_only=True)
    class Meta:
        model = Article
        fields = ('id','user','title','content','create_at','update_at','articlelike','commit')

    
class CommitListSerializer(serializers.ModelSerializer):
    commit = CommitReadSerializer(source = 'commit_set',read_only=True,many = True)
    class Meta:
        model = Article
        fields = ('id',"commit",)

class ArticleLikeUserListSerializer(serializers.ModelSerializer):
    likeuser = serializers.SerializerMethodField()  # 커스텀 필드 추가

    def get_likeuser(self, obj):
        # articlelike_set을 참조하여 관련 User의 username 리스트 생성
        return [like.user.username for like in obj.articlelike_set.all()]

    class Meta:
        model = Article
        fields = ('likeuser',)

