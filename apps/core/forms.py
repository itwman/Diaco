"""
Diaco MES - Core Forms
========================
فرم‌های مدیریت خطوط تولید و ماشین‌آلات.
"""
from django import forms
from .models import ProductionLine, Machine


class ProductionLineForm(forms.ModelForm):
    """فرم ایجاد/ویرایش خط تولید."""

    class Meta:
        model = ProductionLine
        fields = [
            'code', 'name', 'description', 'status',
            'product_type', 'target_capacity_kg', 'line_manager',
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'مثال: LINE-04',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'مثال: خط چهار - نخ اکریلیک',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'توضیحات اختیاری...',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'product_type': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'مثال: نخ پنبه Ne30/1',
            }),
            'target_capacity_kg': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'ظرفیت هدف به کیلوگرم',
            }),
            'line_manager': forms.Select(attrs={'class': 'form-select'}),
        }


class MachineForm(forms.ModelForm):
    """فرم ویرایش ماشین."""

    class Meta:
        model = Machine
        fields = [
            'name', 'production_line', 'machine_type', 'status',
            'location', 'manufacturer', 'model_name', 'year_installed',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'production_line': forms.Select(attrs={'class': 'form-select'}),
            'machine_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_installed': forms.NumberInput(attrs={'class': 'form-control'}),
        }
