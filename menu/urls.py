from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('add/', views.menu_add, name='menu_add'),
    path('<int:pk>/edit/', views.menu_edit, name='menu_edit'),
    path('<int:pk>/delete/', views.menu_delete, name='menu_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
