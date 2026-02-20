from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('line-monitor/', views.line_monitor, name='line_monitor'),
    path('api/line-status/', views.line_monitor_api, name='line_monitor_api'),
    path('floor-map/', views.floor_map, name='floor_map'),
    path('api/floor-map-data/', views.floor_map_api, name='floor_map_api'),
]
