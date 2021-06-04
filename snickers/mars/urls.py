from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('turtle/', views.turtle, name='turtle'),
    path('accounts/register/', views.register, name='register'),
]
