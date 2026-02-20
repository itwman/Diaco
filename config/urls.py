"""
Diaco MES - URL Configuration
==============================
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # داشبورد
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    # ادمین
    path('admin/', admin.site.urls),
    # حساب کاربری
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    # api/accounts legacy - منتقل شد به api/v1/
    # path('api/accounts/', include('apps.accounts.api.urls', namespace='accounts-api')),
    # انبار
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    # سفارشات
    path('orders/', include('apps.orders.urls', namespace='orders')),
    # تولید
    path('production/', include('apps.production.urls', namespace='production')),
    # مدیریت خطوط و ماشین‌آلات
    path('core/', include('apps.core.urls', namespace='core')),
    # ── v2.0: خط تولید نخ فرش ──────────────────────────────────
    path('winding/', include('apps.winding.urls', namespace='winding')),
    path('tfo/', include('apps.tfo.urls', namespace='tfo')),
    path('heatset/', include('apps.heatset.urls', namespace='heatset')),
    # ────────────────────────────────────────────────────────────────
    # نگهداری
    path('maintenance/', include('apps.maintenance.urls', namespace='maintenance')),
    # تبلت اپراتور
    path('tablet/', include('apps.tablet.urls', namespace='tablet')),
    # گزارشات
    path('reports/', include('apps.reports.urls', namespace='reports')),
    # API v1
    path('api/v1/', include('config.api.urls')),
    # AI Analytics
    path('ai/', include('apps.ai_ready.urls', namespace='ai_ready')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    try:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except ImportError:
        pass
