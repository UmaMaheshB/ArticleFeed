from django.urls import path
from articles import views

urlpatterns = [
    path('',views.home,name='home'),
    path('new/',views.ArticleCreateView.as_view(),name='article_create'),
    path('<int:pk>/edit',views.ArticleUpdateView.as_view(),name='article_edit'),
    path('<int:pk>/delete',views.ArticleDeleteView.as_view(),name='article_delete'),
    path('<int:id>/',views.article_details,name='article_details'),
    path('<int:id>/like',views.like_article,name='like_article'),
    path('<int:id>/dislike',views.dislike_article,name='dislike_article'),
    path('<int:id>/block',views.block_article,name='block_article'),
]
