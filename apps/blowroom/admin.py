from django.contrib import admin
from .models import Batch, BatchInput


class BatchInputInline(admin.TabularInline):
    model = BatchInput
    extra = 1
    raw_id_fields = ('fiber_stock',)
    readonly_fields = ('created_at',)


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'machine', 'operator', 'shift', 'total_input_weight', 'output_weight', 'waste_pct', 'status', 'production_date')
    list_filter = ('status', 'production_date', 'machine')
    search_fields = ('batch_number',)
    list_per_page = 25
    date_hierarchy = 'production_date'
    raw_id_fields = ('machine', 'operator', 'order')
    inlines = [BatchInputInline]
    readonly_fields = ('created_at', 'updated_at')
