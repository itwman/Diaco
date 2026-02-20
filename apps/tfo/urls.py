from django.urls import path
from . import views

app_name = 'tfo'

urlpatterns = [
    path('', views.production_list, name='list'),
    path('create/', views.production_create, name='create'),
    path('<int:pk>/', views.production_detail, name='detail'),
    path('<int:pk>/edit/', views.production_edit, name='edit'),
    path('<int:pk>/status/', views.production_change_status, name='status'),
]
