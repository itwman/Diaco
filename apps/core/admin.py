"""
Diaco MES - Core Admin
========================
پنل مدیریت خطوط تولید، ماشین‌آلات، شیفت‌ها، لاگ و اعلان.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ProductionLine, Machine, Shift, LineShiftAssignment, AuditLog, Notification


# ═══════════════════════════════════════════════════════════════
# PRODUCTION LINE (خط تولید)
# ═══════════════════════════════════════════════════════════════

class MachineInline(admin.TabularInline):
    """ماشین‌آلات خط به صورت inline."""
    model = Machine
    extra = 0
    fields = ('code', 'name', 'machine_type', 'status')
    readonly_fields = ('code',)
    show_change_link = True


class LineShiftInline(admin.TabularInline):
    """اختصاص سرشیفت‌ها به صورت inline."""
    model = LineShiftAssignment
    extra = 0
    fields = ('shift', 'supervisor', 'is_active')


@admin.register(ProductionLine)
class ProductionLineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'product_type', 'status_badge', 'line_manager',
                    'machine_count_display', 'target_capacity_kg')
    list_filter = ('status',)
    search_fields = ('code', 'name', 'product_type')
    list_per_page = 20
    inlines = [MachineInline, LineShiftInline]

    fieldsets = (
        ('شناسه', {
            'fields': ('code', 'name', 'description', 'status'),
        }),
        ('محصول و ظرفیت', {
            'fields': ('product_type', 'target_capacity_kg'),
        }),
        ('مدیریت', {
            'fields': ('line_manager',),
        }),
        ('AI-Ready', {
            'fields': ('specs',),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        colors = {'active': '#198754', 'inactive': '#6c757d', 'maintenance': '#fd7e14'}
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:4px; font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'

    def machine_count_display(self, obj):
        return obj.machine_count
    machine_count_display.short_description = 'ماشین فعال'


# ═══════════════════════════════════════════════════════════════
# MACHINE
# ═══════════════════════════════════════════════════════════════

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type_badge', 'production_line', 'status', 'location', 'manufacturer')
    list_filter = ('machine_type', 'status', 'production_line')
    search_fields = ('code', 'name', 'manufacturer')
    list_per_page = 25
    list_editable = ('status', 'production_line')

    fieldsets = (
        ('شناسه', {
            'fields': ('code', 'name'),
        }),
        ('خط تولید', {
            'fields': ('production_line',),
        }),
        ('نوع و وضعیت', {
            'fields': ('machine_type', 'status', 'location'),
        }),
        ('مشخصات', {
            'fields': ('manufacturer', 'model_name', 'year_installed', 'specs'),
            'classes': ('collapse',),
        }),
    )

    def type_badge(self, obj):
        colors = {
            'blowroom': '#6f42c1', 'carding': '#0d6efd', 'passage': '#fd7e14',
            'finisher': '#20c997', 'ring': '#dc3545', 'dyeing': '#e83e8c',
            'boiler': '#795548', 'dryer': '#607d8b',
        }
        color = colors.get(obj.machine_type, '#6c757d')
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:4px; font-size:11px;">{}</span>',
            color, obj.get_machine_type_display()
        )
    type_badge.short_description = 'نوع'


# ═══════════════════════════════════════════════════════════════
# SHIFT
# ═══════════════════════════════════════════════════════════════

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'production_line', 'start_time', 'end_time', 'duration_display', 'is_active')
    list_filter = ('production_line', 'is_active')
    list_editable = ('is_active',)
    ordering = ('production_line', 'start_time')

    def duration_display(self, obj):
        return f"{obj.duration_hours:.1f} ساعت"
    duration_display.short_description = 'مدت'


# ═══════════════════════════════════════════════════════════════
# LINE SHIFT ASSIGNMENT
# ═══════════════════════════════════════════════════════════════

@admin.register(LineShiftAssignment)
class LineShiftAssignmentAdmin(admin.ModelAdmin):
    list_display = ('production_line', 'shift', 'supervisor', 'is_active')
    list_filter = ('production_line', 'is_active')
    list_editable = ('supervisor', 'is_active')


# ═══════════════════════════════════════════════════════════════
# AUDIT LOG
# ═══════════════════════════════════════════════════════════════

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'action', 'table_name', 'record_id', 'ip_address')
    list_filter = ('action', 'table_name', 'created_at')
    search_fields = ('table_name', 'user__username')
    readonly_fields = ('user', 'action', 'table_name', 'record_id', 'old_values', 'new_values', 'ip_address', 'created_at')
    list_per_page = 50
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ═══════════════════════════════════════════════════════════════
# NOTIFICATION
# ═══════════════════════════════════════════════════════════════

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'notif_type', 'is_read', 'created_at')
    list_filter = ('notif_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
    list_per_page = 50
    date_hierarchy = 'created_at'


# ═══════════════════════════════════════════════════════════════
# ADMIN SITE CONFIG
# ═══════════════════════════════════════════════════════════════

admin.site.site_header = 'دیاکو MES | پنل مدیریت'
admin.site.site_title = 'دیاکو'
admin.site.index_title = 'مدیریت سیستم تولید'
