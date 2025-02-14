from django.urls import path
from . import views

app_name = 'ecommerce'


urlpatterns = [
    path('', views.index, name='index'),
    path('products/detail/<int:pk>/', views.product_detail, name='product-detail'),
    path('create-product/', views.product_create, name='product_create'),
    path('delete-product/<int:pk>/', views.product_delete, name='product_delete'),
    path('edit-product/<int:pk>/', views.product_edit, name='product_edit'),
    path('customers/', views.customers, name='customers'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/details/', views.customer_details, name='customer-detail'),
    path('product/like/<int:pk>/', views.product_like_view, name='product-like'),
    path('product/comment/send/<int:pk>/', views.send_product_comment, name='product-comment'),
    path('search/', views.search_view, name='search'),
]