from django.urls import path
from . import views

app_name = 'ai_ready'

urlpatterns = [
    # OEE
    path('oee/<int:machine_id>/', views.api_oee, name='oee'),
    path('oee/<int:machine_id>/range/', views.api_oee_range, name='oee_range'),
    # سری زمانی
    path('timeseries/<int:machine_id>/', views.api_timeseries, name='timeseries'),
    # الگوی توقفات
    path('downtime-pattern/<int:machine_id>/', views.api_downtime_pattern, name='downtime_pattern'),
    # سلامت ناوگان
    path('fleet-health/', views.api_fleet_health, name='fleet_health'),
]
