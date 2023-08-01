from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),         # Путь для представления index
    path('delete_info/', views.delete_info, name='delete_info'),   # Путь для представления delete_info
]
