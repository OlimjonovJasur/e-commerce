from django.urls import path
from . import views

app_name = 'ecommerce'


urlpatterns = [
    path('', views.index, name='index'),
    path('products/detail/<slug:slug>/', views.product_detail, name='product-detail'),
    path('create-product/', views.product_create, name='product_create'),
    path('delete-product/<slug:slug>/', views.product_delete, name='product_delete'),
    path('edit-product/<slug:slug>/', views.product_edit, name='product_edit'),
    path('customers/', views.customers, name='customers'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/details/', views.customer_details, name='customer-detail'),
    path('product/like/<slug:slug>/', views.product_like_view, name='product-like'),
    path('product/comment/send/<slug:slug>/', views.send_product_comment, name='product-comment'),
    path('search/', views.search_view, name='search'),
    path('export-data/', views.export_data, name='export_data')
]