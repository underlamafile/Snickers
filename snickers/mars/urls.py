from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mars/call_click/', views.call_click),
    path('mars/update_boost/', views.update_boost),
    path('register/', views.register, name='register'),
]