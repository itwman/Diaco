"""
Diaco MES - Production Views (تمام مراحل تولید)
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.blowroom.models import Batch as BlowroomBatch
from apps.carding.models import Production as CardingProd
from apps.passage.models import Production as PassageProd
from apps.finisher.models import Production as FinisherProd
from apps.spinning.models import Production as SpinningProd


@login_required
def blowroom_list(request):
    qs = BlowroomBatch.objects.select_related('machine', 'operator').order_by('-production_date')
    return render(request, 'production/blowroom_list.html', {
        'object_list': qs, 'page_title': 'حلاجی', 'breadcrumb_parent': 'خط تولید',
    })


@login_required
def carding_list(request):
    qs = CardingProd.objects.select_related('machine', 'operator').order_by('-production_date')
    return render(request, 'production/carding_list.html', {
        'object_list': qs, 'page_title': 'کاردینگ', 'breadcrumb_parent': 'خط تولید',
    })


@login_required
def passage_list(request):
    qs = PassageProd.objects.select_related('machine', 'operator').order_by('-production_date')
    return render(request, 'production/passage_list.html', {
        'object_list': qs, 'page_title': 'پاساژ', 'breadcrumb_parent': 'خط تولید',
    })


@login_required
def finisher_list(request):
    qs = FinisherProd.objects.select_related('machine', 'operator').order_by('-production_date')
    return render(request, 'production/finisher_list.html', {
        'object_list': qs, 'page_title': 'فینیشر', 'breadcrumb_parent': 'خط تولید',
    })


@login_required
def spinning_list(request):
    qs = SpinningProd.objects.select_related('machine', 'operator').order_by('-production_date')
    return render(request, 'production/spinning_list.html', {
        'object_list': qs, 'page_title': 'رینگ', 'breadcrumb_parent': 'خط تولید',
    })
