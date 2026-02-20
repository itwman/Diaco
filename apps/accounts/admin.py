"""
Diaco MES - Accounts Admin
============================
پنل مدیریت کاربران با پشتیبانی فارسی.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """پنل مدیریت کاربر دیاکو"""

    list_display = (
        'username', 'get_full_name_display', 'role_badge',
        'department', 'phone', 'is_active', 'date_joined',
    )
    list_filter = ('role', 'department', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'national_code', 'phone')
    ordering = ('-date_joined',)
    list_per_page = 25

    # فیلدهای نمایش در صفحه ویرایش
    fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('username', 'password'),
        }),
        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'national_code', 'phone', 'email', 'avatar'),
        }),
        ('نقش و بخش', {
            'fields': ('role', 'department'),
        }),
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('تاریخ‌ها', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )

    # فیلدهای ساخت کاربر جدید
    add_fieldsets = (
        ('اطلاعات ورود', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('اطلاعات شخصی', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'national_code', 'phone'),
        }),
        ('نقش', {
            'classes': ('wide',),
            'fields': ('role', 'department'),
        }),
    )

    def get_full_name_display(self, obj):
        return obj.get_full_name()
    get_full_name_display.short_description = 'نام کامل'

    def role_badge(self, obj):
        """نمایش نقش به صورت badge رنگی"""
        colors = {
            'admin': '#dc3545',
            'manager': '#fd7e14',
            'supervisor': '#0d6efd',
            'operator': '#198754',
            'viewer': '#6c757d',
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:4px; font-size:11px;">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'نقش'
