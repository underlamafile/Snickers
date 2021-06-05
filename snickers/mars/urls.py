from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('turtle/', views.turtle, name='turtle'),
    path('accounts/register/', views.register, name='register'),
    path('test/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]