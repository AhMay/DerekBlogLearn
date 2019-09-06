from django.urls import path
from . import views

app_name = 'smartdoc'

urlpatterns = [
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),

    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),

    path('document/', views.DocumentList.as_view(), name='document_list'),
    path('product/<int:pkr>/document/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('product/<int:pkr>/document/create/', views.DocumentCreateView.as_view(), name='document_create'),
    path('product/<int:pkr>/document/<int:pk>/update/', views.DocumentUpdateView.as_view(), name='document_update'),

    path('document/search/', views.document_search, name='document_search'),
    path('ajax/search/', views.doc_ajax_search, name='doc_ajax_search'),
]