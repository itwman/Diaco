from django.urls import path
from . import views

app_name = 'tablet'

urlpatterns = [
    path('', views.home, name='home'),
    path('select-line/', views.select_line, name='select_line'),
    path('blowroom/', views.blowroom_form, name='blowroom_form'),
    path('carding/', views.carding_form, name='carding_form'),
    path('passage/', views.passage_form, name='passage_form'),
    path('finisher/', views.finisher_form, name='finisher_form'),
    path('spinning/', views.spinning_form, name='spinning_form'),
    # جدید: توقفات
    path('downtime/', views.downtime_form, name='downtime_form'),
    # ── v2.0: تکمیل نخ ──────────────────────────────────────
    path('winding/', views.winding_form, name='winding_form'),
    path('tfo/', views.tfo_form, name='tfo_form'),
    path('heatset/', views.heatset_form, name='heatset_form'),
]
