from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name = 'register'),
    path('login/', views.login_page, name = 'login'),
    path('logout/', views.logout_page, name = 'logout'),
    path('', views.home, name = 'home'),
    path('user/', views.userPage, name = 'user-page'),
    path('products/', views.products, name='products'),
    path('create_order/<int:pk>/', views.create_order, name='create_order'),
    path('update_order/<int:pk>/', views.update_order, name='update_order'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    path('customer/<int:pk>/', views.customer, name='customer'),

]
