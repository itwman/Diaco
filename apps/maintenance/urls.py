from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('workorders/', views.workorder_list, name='workorder_list'),
    path('workorders/create/', views.workorder_create, name='workorder_create'),
    path('workorders/<int:pk>/edit/', views.workorder_edit, name='workorder_edit'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/create/', views.schedule_create, name='schedule_create'),
    path('schedules/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('downtimes/', views.downtime_list, name='downtime_list'),
]
