from django.contrib import admin
from articles.models import Category,Tags,Article,User
# Register your models here.
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Article)
admin.site.register(User)