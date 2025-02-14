from django.urls import path
from . import views
from .views import recommend_products

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('recommend/<int:product_id>/', recommend_products, name='recommend_products'),
]