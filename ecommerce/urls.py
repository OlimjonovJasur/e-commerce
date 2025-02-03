from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/detail/', views.product_detail, name='product-detail'),
    path('customers/', views.customers, name='customers'),
    path('customer/details/', views.customer_details, name='customer-detail'),
]