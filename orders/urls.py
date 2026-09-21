from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('pos/', views.pos, name='pos'),
    path('pos/add/<int:item_id>/', views.pos_add, name='pos_add'),
    path('pos/remove/<int:item_id>/', views.pos_remove, name='pos_remove'),
    path('pos/clear/', views.pos_clear, name='pos_clear'),
    path('pos/checkout/', views.pos_checkout, name='pos_checkout'),
    path('<int:pk>/receipt/', views.receipt, name='receipt'),
    path('', views.order_history, name='order_history'),
]
