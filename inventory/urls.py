from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('add/', views.stock_add, name='stock_add'),
    path('<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('<int:pk>/adjust/', views.stock_adjust, name='stock_adjust'),
]
