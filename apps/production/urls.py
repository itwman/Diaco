from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('blowroom/', views.blowroom_list, name='blowroom_list'),
    path('carding/', views.carding_list, name='carding_list'),
    path('passage/', views.passage_list, name='passage_list'),
    path('finisher/', views.finisher_list, name='finisher_list'),
    path('spinning/', views.spinning_list, name='spinning_list'),
]
