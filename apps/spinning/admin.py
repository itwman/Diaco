from django.contrib import admin
from django.utils.html import format_html
from .models import Production, TravelerReplacement


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = (
        'batch_number', 'finisher_production', 'machine', 'yarn_count',
        'twist_tpm', 'breakage_count', 'efficiency_display', 'status', 'production_date',
    )
    list_filter = ('status', 'production_date', 'machine', 'twist_direction')
    search_fields = ('batch_number',)
    list_per_page = 25
    date_hierarchy = 'production_date'
    raw_id_fields = ('machine', 'operator', 'finisher_production', 'order')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('شناسه', {
            'fields': ('batch_number', 'finisher_production', 'order'),
        }),
        ('عملیات', {
            'fields': ('machine', 'operator', 'shift', 'production_date'),
        }),
        ('پارامترهای رینگ', {
            'fields': ('spindle_speed_rpm', 'twist_tpm', 'twist_direction', 'yarn_count'),
        }),
        ('شیطانک', {
            'fields': ('traveler_number', 'traveler_type', 'ring_diameter'),
            'classes': ('collapse',),
        }),
        ('تولید', {
            'fields': ('input_weight', 'output_weight', 'num_spindles_active', 'num_spindles_total'),
        }),
        ('کیفیت و عملکرد', {
            'fields': ('breakage_count', 'efficiency_pct'),
        }),
        ('وضعیت', {
            'fields': ('status', 'started_at', 'completed_at', 'notes', 'metadata'),
        }),
    )

    def efficiency_display(self, obj):
        if obj.efficiency_pct is None:
            return '-'
        pct = float(obj.efficiency_pct)
        color = '#198754' if pct >= 85 else '#fd7e14' if pct >= 70 else '#dc3545'
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}%</span>',
            color, int(pct)
        )
    efficiency_display.short_description = 'راندمان'


@admin.register(TravelerReplacement)
class TravelerReplacementAdmin(admin.ModelAdmin):
    list_display = ('machine', 'new_traveler', 'reason', 'running_hours', 'replaced_at', 'next_due_at')
    list_filter = ('reason', 'machine')
    search_fields = ('machine__code', 'new_traveler')
    list_per_page = 25
    raw_id_fields = ('machine', 'operator')
    readonly_fields = ('created_at',)
