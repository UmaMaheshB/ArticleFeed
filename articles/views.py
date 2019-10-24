from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView,UpdateView,DeleteView,ListView
from articles.models import Article,User
from .forms import ArticleForm,UserAccounForm


@method_decorator(login_required, name='dispatch')
class MyArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/my_articles.html'

    def get_queryset(self):
        user_articles = Article.objects.filter(user=self.request.user)
        return user_articles


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request,"article saved successfully.")
        # form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'

    def get_queryset(self):
        queryset = Article.objects.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = '/articles/'
    
    def get_queryset(self):
        queryset = Article.objects.filter(user=self.request.user)
        return queryset
    
    def get(self, request, *args, **kwargs):
        self.post(self,request,*args,**kwargs)
        messages.success(request,"article deleted successfully..")
        return redirect(reverse('home'))
        
    
def home(request):
    if request.user.is_authenticated:
        articles = Article.objects.filter(category=request.user.article_preferences)
        articles = articles.exclude(blocked_by__in=[request.user])
    else:
        articles = Article.objects.all()
    return render(request,'articles/home.html',{'articles':articles})


def article_details(request,id):
    article = get_object_or_404(Article,id=id)
    total_likes = article.likes_count()
    total_dislikes = article.dislikes_count()
    context = {}
    if article.likes.filter(id=request.user.id).exists():
        context['is_liked'] = True
    if article.dislikes.filter(id=request.user.id).exists():
        context['is_disliked'] = True
    
    context['article'] = article
    context['total_likes'] = total_likes
    context['total_dislikes'] = total_dislikes
    return render(request,'articles/article_details.html',context)


@login_required
def like_article(request,id):
    article = get_object_or_404(Article,id=id)
    if article.dislikes.filter(id=request.user.id).exists():
        article.dislikes.remove(request.user)
    if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect(reverse('article_details',args=[article.id]))


@login_required
def dislike_article(request,id):
    article = get_object_or_404(Article,id=id)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    if article.dislikes.filter(id=request.user.id).exists():
        article.dislikes.remove(request.user)
    else:
        article.dislikes.add(request.user)
    return redirect(reverse('article_details',args=[article.id]))


@login_required
def block_article(request,id):
    article = get_object_or_404(Article, id=id)
    if article:
        article.blocked_by.add(request.user)
    return HttpResponseRedirect(article.get_absolute_url())


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserAccounForm
    template_name = 'account/account_settings.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'details saved')
        return redirect(reverse('home'))
