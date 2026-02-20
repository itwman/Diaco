from django.urls import path
from . import views

app_name = 'heatset'

urlpatterns = [
    path('', views.batch_list, name='list'),
    path('create/', views.batch_create, name='create'),
    path('<int:pk>/', views.batch_detail, name='detail'),
    path('<int:pk>/edit/', views.batch_edit, name='edit'),
    path('<int:pk>/status/', views.batch_change_status, name='status'),
    path('<int:pk>/log/add/', views.cycle_log_add, name='log_add'),
    path('<int:pk>/log/data/', views.cycle_log_data, name='log_data'),
]
