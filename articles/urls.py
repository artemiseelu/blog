from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.home, name='home'),  # 例如: /
    
    # 文章列表
    path('articles/', views.article_list, name='article_list'),  # 例如: /articles/
    
    # 发布文章 - 移到详情页前面
    path('article/upload/', views.article_upload, name='article_upload'),  # 例如: /article/upload/
    
    # 文章详情
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),  # 例如: /article/my-first-post/
    
    # 编辑文章
    path('article/<slug:slug>/edit/', views.article_edit, name='article_edit'),  # 例如: /article/my-first-post/edit/
    
    # 删除文章
    path('article/<slug:slug>/delete/', views.article_delete, name='article_delete'),  # 例如: /article/my-first-post/delete/
    path('admin/generate-slug/', views.generate_slug_view, name='generate_slug'),
    path('resume/', views.resume2, name='resume'),
    path('resume2/', views.resume2, name='resume2'),
    path('resume2/<str:lang>/', views.resume2, name='resume2_with_lang'),
]
