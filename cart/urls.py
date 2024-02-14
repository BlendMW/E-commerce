from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('ajax/update/', views.ajax_cart_update, name='ajax_cart_update'),
    path('ajax/add/<int:product_id>/', views.ajax_cart_add, name='ajax_cart_add'),
    path('ajax/remove/', views.ajax_cart_remove, name='ajax_cart_remove'),

]
