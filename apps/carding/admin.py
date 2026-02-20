from django.contrib import admin
from .models import Production


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'blowroom_batch', 'machine', 'operator', 'sliver_count', 'neps_count', 'status', 'production_date')
    list_filter = ('status', 'production_date', 'machine')
    search_fields = ('batch_number',)
    list_per_page = 25
    date_hierarchy = 'production_date'
    raw_id_fields = ('machine', 'operator', 'blowroom_batch', 'order')
    readonly_fields = ('created_at', 'updated_at')
