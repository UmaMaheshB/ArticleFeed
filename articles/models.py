from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class User(AbstractUser):
    mobile = models.CharField(max_length=13)
    birth_date = models.DateField(null=True, blank=True)
    article_preferences = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)

# class Image(models.Model):
#     url = models.CharField(max_length=300)
#     def __str__(self):
#         return self.url

class Tags(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Article(models.Model):
    name = models.CharField("Article Name",max_length=100)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=500,default="http://cloudrangers.com/blog/wp-content/uploads/2017/08/blog_default.png")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank=True,related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    blocked_by = models.ManyToManyField(User,blank=True,related_name='blocked_users')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_details', args=[str(self.id)])

    def likes_count(self):
        return self.likes.count()
    def dislikes_count(self):
        return self.dislikes.count()
