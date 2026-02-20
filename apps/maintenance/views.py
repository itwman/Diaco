from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from apps.core.models import Machine
from apps.core.batch_utils import next_batch_number
from .models import WorkOrder, Schedule, DowntimeLog

User = get_user_model()


def _next_wo_number():
    """شماره دستور کار: WO-YYYYMMDD-NNN"""
    return next_batch_number('WO')


@login_required
def workorder_list(request):
    qs = WorkOrder.objects.select_related('machine', 'assigned_to').order_by('-created_at')
    status_f = request.GET.get('status', '')
    priority_f = request.GET.get('priority', '')
    type_f = request.GET.get('type', '')
    if status_f:
        qs = qs.filter(status=status_f)
    if priority_f:
        qs = qs.filter(priority=priority_f)
    if type_f:
        qs = qs.filter(wo_type=type_f)
    return render(request, 'maintenance/workorder_list.html', {
        'object_list': qs,
        'page_title': 'دستورهای کار',
        'breadcrumb_parent': 'نگهداری',
        'status_choices': WorkOrder.Status.choices,
        'priority_choices': WorkOrder.Priority.choices,
        'type_choices': WorkOrder.WOType.choices,
        'status_filter': status_f,
        'priority_filter': priority_f,
        'type_filter': type_f,
        'machines': Machine.objects.filter(status='active').order_by('code'),
        'users': User.objects.filter(is_active=True).order_by('first_name', 'username'),
    })


@login_required
@require_POST
def workorder_create(request):
    """ایجاد دستور کار جدید"""
    try:
        WorkOrder.objects.create(
            wo_number=_next_wo_number(),
            machine_id=request.POST['machine'],
            title=request.POST['title'].strip(),
            description=request.POST.get('description', '').strip(),
            wo_type=request.POST.get('wo_type', 'corrective'),
            priority=request.POST.get('priority', 'medium'),
            status=request.POST.get('status', 'open'),
            reported_by=request.user,
            assigned_to_id=request.POST.get('assigned_to') or None,
            downtime_min=request.POST.get('downtime_min') or None,
            cost_parts=request.POST.get('cost_parts') or 0,
            cost_labor=request.POST.get('cost_labor') or 0,
            notes=request.POST.get('notes', '').strip(),
        )
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def workorder_edit(request, pk):
    """ویرایش دستور کار"""
    wo = get_object_or_404(WorkOrder, pk=pk)
    try:
        wo.machine_id = request.POST['machine']
        wo.title = request.POST['title'].strip()
        wo.description = request.POST.get('description', '').strip()
        wo.wo_type = request.POST.get('wo_type', wo.wo_type)
        wo.priority = request.POST.get('priority', wo.priority)
        wo.status = request.POST.get('status', wo.status)
        wo.assigned_to_id = request.POST.get('assigned_to') or None
        wo.downtime_min = request.POST.get('downtime_min') or None
        wo.cost_parts = request.POST.get('cost_parts') or 0
        wo.cost_labor = request.POST.get('cost_labor') or 0
        wo.notes = request.POST.get('notes', '').strip()
        wo.save()
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def schedule_list(request):
    qs = Schedule.objects.select_related('machine', 'assigned_to').order_by('next_due_at')
    return render(request, 'maintenance/schedule_list.html', {
        'object_list': qs,
        'page_title': 'برنامه PM',
        'breadcrumb_parent': 'نگهداری',
        'machines': Machine.objects.filter(status='active').order_by('code'),
        'users': User.objects.filter(is_active=True).order_by('first_name', 'username'),
        'frequency_choices': Schedule.Frequency.choices,
        'type_choices': Schedule.MaintenanceType.choices,
        'priority_choices': Schedule.Priority.choices,
    })


@login_required
@require_POST
def schedule_create(request):
    """ایجاد برنامه PM جدید"""
    from django.utils import timezone
    import jdatetime

    def parse_dt(val):
        """تبدیل تاریخ میلادی YYYY-MM-DD به datetime"""
        if not val:
            return None
        try:
            from datetime import datetime
            return timezone.make_aware(datetime.strptime(val, '%Y-%m-%d'))
        except Exception:
            return None

    try:
        Schedule.objects.create(
            machine_id=request.POST['machine'],
            title=request.POST['title'].strip(),
            description=request.POST.get('description', '').strip(),
            maintenance_type=request.POST.get('maintenance_type', 'preventive'),
            frequency=request.POST.get('frequency', 'monthly'),
            custom_days=request.POST.get('custom_days') or None,
            next_due_at=parse_dt(request.POST.get('next_due_at_g')) or timezone.now(),
            last_done_at=parse_dt(request.POST.get('last_done_at_g')),
            assigned_to_id=request.POST.get('assigned_to') or None,
            priority=request.POST.get('priority', 'medium'),
            is_active=True,
        )
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def schedule_edit(request, pk):
    """ویرایش برنامه PM"""
    from django.utils import timezone

    def parse_dt(val):
        if not val:
            return None
        try:
            from datetime import datetime
            return timezone.make_aware(datetime.strptime(val, '%Y-%m-%d'))
        except Exception:
            return None

    sch = get_object_or_404(Schedule, pk=pk)
    try:
        sch.machine_id = request.POST['machine']
        sch.title = request.POST['title'].strip()
        sch.description = request.POST.get('description', '').strip()
        sch.maintenance_type = request.POST.get('maintenance_type', sch.maintenance_type)
        sch.frequency = request.POST.get('frequency', sch.frequency)
        sch.custom_days = request.POST.get('custom_days') or None
        next_due = parse_dt(request.POST.get('next_due_at_g'))
        if next_due:
            sch.next_due_at = next_due
        sch.last_done_at = parse_dt(request.POST.get('last_done_at_g'))
        sch.assigned_to_id = request.POST.get('assigned_to') or None
        sch.priority = request.POST.get('priority', sch.priority)
        sch.is_active = request.POST.get('is_active', '1') == '1'
        sch.save()
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def downtime_list(request):
    qs = DowntimeLog.objects.select_related('machine', 'shift').order_by('-start_time')
    return render(request, 'maintenance/downtime_list.html', {
        'object_list': qs, 'page_title': 'لاگ توقفات', 'breadcrumb_parent': 'نگهداری',
    })
