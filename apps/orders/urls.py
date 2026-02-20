from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # ── مشتریان ──────────────────────────────────────────
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customers/<int:pk>/json/', views.customer_get_json, name='customer_json'),

    # ── سفارشات ──────────────────────────────────────────
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('<int:pk>/status/', views.order_change_status, name='order_status'),
    path('<int:pk>/cancel/', views.order_cancel, name='order_cancel'),

    # ── شیدهای رنگی ──────────────────────────────────────
    path('shades/', views.shade_list, name='shade_list'),
    path('shades/create/', views.shade_create, name='shade_create'),
    path('shades/<int:pk>/edit/', views.shade_edit, name='shade_edit'),
    path('shades/<int:pk>/delete/', views.shade_delete, name='shade_delete'),
]
