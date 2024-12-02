from django.contrib import admin
from .models import ArticleType, Article,Commit
# Register your models here.

admin.site.register(ArticleType)
admin.site.register(Article)
admin.site.register(Commit)