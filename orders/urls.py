from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.order_list, name='order_list'),
    path('detail/<int:id>/', views.order_details, name='order_details'),
    path('track/', views.track_order, name='track_order'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('order-history/', views.order_history, name='order_history'),
    path('order-history/<int:order_id>/', views.order_history, name='order_history'),
    path('order/update/<int:order_id>/', views.update_order, name='update_order'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    
]
