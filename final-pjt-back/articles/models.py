from django.db import models
from django.conf import settings
# Create your models here.

class ArticleType(models.Model): # 어떤 종류의 게시글인지 ex(자유게시판, 주식or 적금 or 예금 추천글, 등등)
    articletype = models.CharField(max_length=255)
    def __str__(self):
        return self.articletype

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='article_user')
    article_type = models.ForeignKey(ArticleType,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class ArticleLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)



class Commit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content

