from django.forms import ModelForm
from .models import Article, User
from django import forms

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['user','likes','dislikes','blocked_by']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','mobile','birth_date','article_preferences']

    def signup(self, request, user):
        user.mobile = self.cleaned_data['mobile']
        user.article_preferences = self.cleaned_data['article_preferences']
        user.save()


class UserAccounForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','mobile','birth_date','article_preferences']