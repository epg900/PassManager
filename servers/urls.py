from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from servers import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='servers/login.html'), name='login'),
    path('logout/', views.signout , name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_server, name='add_server'),
    path('edit/<int:pk>/', views.edit_server, name='edit_server'),
    path('delete/<int:pk>/', views.delete_server, name='delete_server'),
    path('getpassstr/', views.get_pass_str, name='get_pass_str'),
    path('checkpass/', views.checkpass, name='checkpass'),
    path('down_config/<int:pk>/', views.download_config, name='download_config'),
]
