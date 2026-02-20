"""
Diaco MES - Core URLs
=======================
مسیرهای مدیریت خطوط تولید، ماشین‌آلات و شیفت‌ها.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # ── خطوط تولید ──────────────────────────────────
    path('lines/', views.line_list, name='line_list'),
    path('lines/create/', views.line_create, name='line_create'),
    path('lines/<int:pk>/', views.line_detail, name='line_detail'),
    path('lines/<int:pk>/edit/', views.line_edit, name='line_edit'),

    # ── ماشین‌آلات ───────────────────────────────────
    path('machines/', views.machine_list, name='machine_list'),
    path('machines/create/', views.machine_create, name='machine_create'),
    path('machines/<int:pk>/edit/', views.machine_edit, name='machine_edit'),

    # ── شیفت‌ها ──────────────────────────────────────
    path('shifts/', views.shift_list, name='shift_list'),
]
