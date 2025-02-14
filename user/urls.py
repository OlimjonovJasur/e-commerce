from django.urls import path
from . import views

app_name = 'user'


urlpatterns = [
    path('login-oauth-page/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page')
]