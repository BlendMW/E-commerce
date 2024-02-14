from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('products/add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('ajax/get-variant-quantity/', views.get_variant_quantity, name='get_variant_quantity'),
    path('management/', views.product_management, name='product_management'),
    path('view/<int:id>/', views.product_view, name='product_view'),
]