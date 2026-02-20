from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # گزارشات پایه
    path('production/',      views.production_daily,        name='production_daily'),
    path('materials/',       views.material_consumption,    name='material_consumption'),
    path('downtime/',        views.downtime_report,          name='downtime_report'),
    # گزارشات R1
    path('waste/',           views.waste_report,            name='waste_report'),
    path('oee/',             views.oee_report,              name='oee_report'),
    path('compare/',         views.compare_periods,         name='compare_periods'),
    path('operators/',       views.operator_performance,    name='operator_performance'),
    # گزارشات v2.0 (فاز D)
    path('winding/',         views.winding_report,          name='winding_report'),
    path('tfo/',             views.tfo_report,              name='tfo_report'),
    path('heatset/',         views.heatset_report,          name='heatset_report'),
    path('chain/',           views.production_chain,        name='production_chain'),
    # خروجی Excel
    path('export/production/', views.export_production_excel, name='export_production'),
    path('export/winding/',    views.export_winding_excel,    name='export_winding'),
    path('export/heatset/',    views.export_heatset_excel,    name='export_heatset'),
    path('export/downtime/',   views.export_downtime_excel,   name='export_downtime'),
]
