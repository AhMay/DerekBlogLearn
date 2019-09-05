from django.urls import path
from . import views
app_name = 'blog'

urlpatterns=[
    #所有文章列表-不需要登录
    path('', views.ArticleListView.as_view(), name='article_list'),
    #文章详情-不需要登录
    path('article/<int:pk>/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    #文章创建-需要登录
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    #更新文章，需要登录
    path('article/<int:pk>/<slug:slug>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    #已发表文章列表(含编辑）-需要登录
    path('admin/',views.PublishedArticleListView.as_view(), name='published_article_list'),
    #草稿箱里面的文章-需要登录
    path('draft/', views.ArticleDraftListView.as_view(), name='article_draft_list'),
    #发表文章--需要登录
    path('article/<int:pk>/<slug:slug>/publish/', views.article_publish, name='article_publish'),
    path('article/<int:pk>/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),

    #类别列表
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('tags/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('search/', views.article_search, name='article_search'),
    path('article/like/', views.article_like, name='article_like'),
]