from django.contrib import admin
from django.utils.html import format_html
from .models import Schedule, WorkOrder, DowntimeLog, MachineServiceDate


# ═══════════════════════════════════════════════════════════════
# SCHEDULE
# ═══════════════════════════════════════════════════════════════

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('machine', 'title', 'maintenance_type', 'frequency', 'priority_badge', 'next_due_at', 'overdue_badge', 'is_active')
    list_filter = ('maintenance_type', 'frequency', 'priority', 'is_active', 'machine')
    search_fields = ('title', 'machine__code')
    list_per_page = 25
    raw_id_fields = ('machine', 'assigned_to')
    readonly_fields = ('created_at', 'updated_at')

    def priority_badge(self, obj):
        colors = {'low': '#6c757d', 'medium': '#0d6efd', 'high': '#fd7e14', 'critical': '#dc3545'}
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; border-radius:4px; font-size:11px;">{}</span>',
            colors.get(obj.priority, '#6c757d'), obj.get_priority_display()
        )
    priority_badge.short_description = 'اولویت'

    def overdue_badge(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color:#dc3545; font-weight:bold;">⚠ عقب‌افتاده</span>')
        return format_html('<span style="color:#198754;">✓</span>')
    overdue_badge.short_description = 'وضعیت موعد'


# ═══════════════════════════════════════════════════════════════
# WORK ORDER
# ═══════════════════════════════════════════════════════════════

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('wo_number', 'machine', 'title', 'wo_type', 'priority_badge', 'status_badge', 'downtime_min', 'total_cost_display')
    list_filter = ('status', 'wo_type', 'priority', 'machine')
    search_fields = ('wo_number', 'title', 'machine__code')
    list_per_page = 25
    raw_id_fields = ('machine', 'reported_by', 'assigned_to', 'schedule')
    readonly_fields = ('created_at', 'updated_at')

    def priority_badge(self, obj):
        colors = {'low': '#6c757d', 'medium': '#0d6efd', 'high': '#fd7e14', 'critical': '#dc3545'}
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; border-radius:4px; font-size:11px;">{}</span>',
            colors.get(obj.priority, '#6c757d'), obj.get_priority_display()
        )
    priority_badge.short_description = 'اولویت'

    def status_badge(self, obj):
        colors = {'open': '#0d6efd', 'in_progress': '#fd7e14', 'waiting_parts': '#6f42c1', 'completed': '#198754', 'cancelled': '#dc3545'}
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; border-radius:4px; font-size:11px;">{}</span>',
            colors.get(obj.status, '#6c757d'), obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'

    def total_cost_display(self, obj):
        total = obj.total_cost
        if total:
            return f"{total:,.0f} ریال"
        return '-'
    total_cost_display.short_description = 'هزینه کل'


# ═══════════════════════════════════════════════════════════════
# DOWNTIME LOG
# ═══════════════════════════════════════════════════════════════

@admin.register(DowntimeLog)
class DowntimeLogAdmin(admin.ModelAdmin):
    list_display = ('machine', 'reason_category', 'reason_detail', 'duration_min', 'production_loss', 'shift', 'start_time')
    list_filter = ('reason_category', 'machine', 'shift')
    search_fields = ('reason_detail', 'machine__code')
    list_per_page = 25
    raw_id_fields = ('machine', 'operator', 'work_order')
    readonly_fields = ('created_at',)


# ═══════════════════════════════════════════════════════════════
# MACHINE SERVICE DATE
# ═══════════════════════════════════════════════════════════════

@admin.register(MachineServiceDate)
class MachineServiceDateAdmin(admin.ModelAdmin):
    list_display = ('machine', 'service_type', 'service_date', 'next_service', 'performed_by', 'cost')
    list_filter = ('machine', 'service_date')
    search_fields = ('service_type', 'machine__code', 'performed_by')
    list_per_page = 25
    date_hierarchy = 'service_date'
    readonly_fields = ('created_at',)
