"""
Diaco MES - Core Views
========================
نمای مدیریت خطوط تولید، ماشین‌آلات و شیفت‌ها.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Q

from .models import ProductionLine, Machine, Shift, LineShiftAssignment
from .forms import ProductionLineForm, MachineForm


# ═══════════════════════════════════════════════════════════════
# خطوط تولید
# ═══════════════════════════════════════════════════════════════

@login_required
def line_list(request):
    """لیست خطوط تولید با آمار ماشین‌آلات."""
    lines = ProductionLine.objects.annotate(
        total_machines=Count('machines'),
        active_machines=Count('machines', filter=Q(machines__status='active')),
        maintenance_machines=Count('machines', filter=Q(machines__status='maintenance')),
    ).order_by('code')

    context = {
        'object_list': lines,
        'page_title': 'خطوط تولید',
        'breadcrumb_parent': 'مدیریت',
    }
    return render(request, 'core/line_list.html', context)


@login_required
def line_detail(request, pk):
    """جزئیات خط تولید + ماشین‌آلات + شیفت‌ها."""
    line = get_object_or_404(ProductionLine, pk=pk)
    machines = Machine.objects.filter(production_line=line).order_by('machine_type', 'code')
    shifts = Shift.objects.filter(production_line=line).order_by('start_time')
    assignments = LineShiftAssignment.objects.filter(
        production_line=line
    ).select_related('shift', 'supervisor')

    # آمار ماشین‌ها
    machine_stats = {
        'total': machines.count(),
        'active': machines.filter(status='active').count(),
        'maintenance': machines.filter(status='maintenance').count(),
        'inactive': machines.filter(status='inactive').count(),
    }

    # دسته‌بندی ماشین‌ها بر اساس نوع
    machine_groups = {}
    for m in machines:
        type_display = m.get_machine_type_display()
        if type_display not in machine_groups:
            machine_groups[type_display] = []
        machine_groups[type_display].append(m)

    context = {
        'line': line,
        'machines': machines,
        'machine_groups': machine_groups,
        'machine_stats': machine_stats,
        'shifts': shifts,
        'assignments': assignments,
        'page_title': f'خط تولید {line.code}',
        'breadcrumb_parent': 'خطوط تولید',
    }
    return render(request, 'core/line_detail.html', context)


@login_required
def line_create(request):
    """ایجاد خط تولید جدید."""
    if request.method == 'POST':
        form = ProductionLineForm(request.POST)
        if form.is_valid():
            line = form.save()
            messages.success(request, f'خط تولید «{line.name}» با موفقیت ایجاد شد.')
            return redirect('core:line_detail', pk=line.pk)
    else:
        form = ProductionLineForm()

    context = {
        'form': form,
        'page_title': 'ایجاد خط تولید جدید',
        'breadcrumb_parent': 'خطوط تولید',
        'is_edit': False,
    }
    return render(request, 'core/line_form.html', context)


@login_required
def line_edit(request, pk):
    """ویرایش خط تولید."""
    line = get_object_or_404(ProductionLine, pk=pk)
    if request.method == 'POST':
        form = ProductionLineForm(request.POST, instance=line)
        if form.is_valid():
            form.save()
            messages.success(request, f'خط تولید «{line.name}» بروزرسانی شد.')
            return redirect('core:line_detail', pk=line.pk)
    else:
        form = ProductionLineForm(instance=line)

    context = {
        'form': form,
        'line': line,
        'page_title': f'ویرایش {line.code}',
        'breadcrumb_parent': 'خطوط تولید',
        'is_edit': True,
    }
    return render(request, 'core/line_form.html', context)


# ═══════════════════════════════════════════════════════════════
# ماشین‌آلات
# ═══════════════════════════════════════════════════════════════

@login_required
def machine_list(request):
    """لیست تمام ماشین‌آلات با فیلتر."""
    machines = Machine.objects.select_related('production_line').order_by('production_line', 'machine_type', 'code')

    # فیلتر بر اساس خط
    line_filter = request.GET.get('line')
    if line_filter:
        machines = machines.filter(production_line__code=line_filter)

    # فیلتر بر اساس نوع
    type_filter = request.GET.get('type')
    if type_filter:
        machines = machines.filter(machine_type=type_filter)

    # فیلتر بر اساس وضعیت
    status_filter = request.GET.get('status')
    if status_filter:
        machines = machines.filter(status=status_filter)

    lines = ProductionLine.objects.all().order_by('code')

    context = {
        'object_list': machines,
        'lines': lines,
        'machine_types': Machine.MachineType.choices,
        'machine_statuses': Machine.Status.choices,
        'current_line': line_filter,
        'current_type': type_filter,
        'current_status': status_filter,
        'page_title': 'ماشین‌آلات',
        'breadcrumb_parent': 'مدیریت',
    }
    return render(request, 'core/machine_list.html', context)


@login_required
def machine_edit(request, pk):
    """ویرایش ماشین — AJAX یا فرم"""
    machine = get_object_or_404(Machine, pk=pk)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
               request.accepts('application/json') or \
               request.POST.get('_ajax')
    if request.method == 'POST':
        from django.http import JsonResponse as JR
        try:
            machine.code = request.POST.get('code', machine.code).strip().upper()
            machine.name = request.POST.get('name', machine.name).strip()
            machine.machine_type = request.POST.get('machine_type', machine.machine_type)
            machine.status = request.POST.get('status', machine.status)
            machine.production_line_id = request.POST.get('production_line') or None
            machine.manufacturer = request.POST.get('manufacturer', '').strip()
            machine.model_name = request.POST.get('model_name', '').strip()
            machine.location = request.POST.get('location', '').strip()
            yr = request.POST.get('year_installed', '')
            machine.year_installed = int(yr) if yr.strip() else None
            machine.save()
            # اگر AJAX باشد JSON برگردان
            try:
                return JR({'ok': True})
            except Exception:
                pass
        except Exception as e:
            try:
                return JR({'ok': False, 'error': str(e)}, status=400)
            except Exception:
                pass
        messages.success(request, f'ماشین «{machine.code}» بروزرسانی شد.')
        return redirect('core:machine_list')

    form = MachineForm(instance=machine)
    return render(request, 'core/machine_form.html', {
        'form': form, 'machine': machine,
        'page_title': f'ویرایش {machine.code}',
        'breadcrumb_parent': 'ماشین‌آلات',
    })


@login_required
def machine_create(request):
    """افزودن ماشین جدید — AJAX"""
    if request.method != 'POST':
        from django.http import JsonResponse as JR
        return JR({'ok': False, 'error': 'POST required'}, status=405)
    from django.http import JsonResponse as JR
    try:
        yr = request.POST.get('year_installed', '')
        machine = Machine.objects.create(
            code=request.POST['code'].strip().upper(),
            name=request.POST['name'].strip(),
            machine_type=request.POST['machine_type'],
            status=request.POST.get('status', 'active'),
            production_line_id=request.POST.get('production_line') or None,
            manufacturer=request.POST.get('manufacturer', '').strip(),
            model_name=request.POST.get('model_name', '').strip(),
            location=request.POST.get('location', '').strip(),
            year_installed=int(yr) if yr.strip() else None,
        )
        return JR({'ok': True, 'id': machine.id, 'code': machine.code})
    except Exception as e:
        return JR({'ok': False, 'error': str(e)}, status=400)


# ═══════════════════════════════════════════════════════════════
# شیفت‌ها
# ═══════════════════════════════════════════════════════════════

@login_required
def shift_list(request):
    """لیست شیفت‌ها به تفکیک خط."""
    shifts = Shift.objects.select_related('production_line').order_by('production_line', 'start_time')
    assignments = LineShiftAssignment.objects.select_related(
        'production_line', 'shift', 'supervisor'
    ).order_by('production_line', 'shift__start_time')

    context = {
        'object_list': shifts,
        'assignments': assignments,
        'page_title': 'شیفت‌ها و سرشیفت‌ها',
        'breadcrumb_parent': 'مدیریت',
    }
    return render(request, 'core/shift_list.html', context)
