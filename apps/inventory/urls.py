from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # ── الیاف ────────────────────────────────────────────
    path('fibers/', views.fiber_list, name='fiber_list'),
    path('fibers/receive/', views.fiber_receive, name='fiber_receive'),
    path('fibers/<int:pk>/issue/', views.fiber_issue, name='fiber_issue'),
    path('fibers/<int:pk>/adjust/', views.fiber_adjust, name='fiber_adjust'),
    path('fibers/<int:pk>/json/', views.fiber_get_json, name='fiber_json'),
    path('fibers/<int:pk>/transactions/', views.fiber_transactions, name='fiber_transactions'),

    # ── رنگ ──────────────────────────────────────────────
    path('dyes/', views.dye_list, name='dye_list'),
    path('dyes/create/', views.dye_create, name='dye_create'),
    path('dyes/<int:pk>/edit/', views.dye_edit, name='dye_edit'),

    # ── مواد شیمیایی ─────────────────────────────────────
    path('chemicals/', views.chemical_list, name='chemical_list'),
    path('chemicals/create/', views.chemical_create, name='chemical_create'),
    path('chemicals/<int:pk>/edit/', views.chemical_edit, name='chemical_edit'),
]
