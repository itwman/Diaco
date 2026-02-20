from django.contrib import admin
from django.utils.html import format_html
from .models import Batch, ChemicalUsage, BoilerLog, DryerLog


class ChemicalUsageInline(admin.TabularInline):
    model = ChemicalUsage
    extra = 1
    raw_id_fields = ('dye_stock', 'chemical_stock')
    fields = ('sequence_order', 'material_type', 'dye_stock', 'chemical_stock', 'quantity_used', 'unit', 'step_name')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'color_shade', 'machine', 'fiber_weight', 'temperature', 'ph_value', 'quality_badge', 'status', 'production_date')
    list_filter = ('status', 'quality_result', 'production_date', 'machine')
    search_fields = ('batch_number', 'color_shade__code')
    list_per_page = 25
    date_hierarchy = 'production_date'
    raw_id_fields = ('machine', 'operator', 'order', 'color_shade')
    inlines = [ChemicalUsageInline]
    readonly_fields = ('created_at', 'updated_at')

    def quality_badge(self, obj):
        if not obj.quality_result:
            return '-'
        colors = {'pass': '#198754', 'fail': '#dc3545', 'conditional': '#fd7e14'}
        color = colors.get(obj.quality_result, '#6c757d')
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; border-radius:4px; font-size:11px;">{}</span>',
            color, obj.get_quality_result_display()
        )
    quality_badge.short_description = 'کیفیت'


@admin.register(BoilerLog)
class BoilerLogAdmin(admin.ModelAdmin):
    list_display = ('machine', 'log_date', 'shift', 'pressure_bar', 'temperature_c', 'water_level', 'fuel_consumed', 'running_hours', 'status')
    list_filter = ('status', 'machine', 'log_date')
    list_per_page = 25
    date_hierarchy = 'log_date'
    raw_id_fields = ('machine', 'operator')


@admin.register(DryerLog)
class DryerLogAdmin(admin.ModelAdmin):
    list_display = ('machine', 'log_date', 'shift', 'dyeing_batch', 'temperature_c', 'duration_min', 'humidity_pct', 'status')
    list_filter = ('status', 'machine', 'log_date')
    list_per_page = 25
    date_hierarchy = 'log_date'
    raw_id_fields = ('machine', 'operator', 'dyeing_batch')
