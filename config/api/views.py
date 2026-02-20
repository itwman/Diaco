"""
Diaco MES - API ViewSets
==========================
تمام ViewSetها در یک فایل مرکزی.
هر ViewSet: ModelViewSet + فیلتر + جستجو + ترتیب.
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

# ── Accounts ─────────────────────────────────────────────
from apps.accounts.models import User
from apps.accounts.api.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'department']
    search_fields = ['username', 'first_name', 'last_name']


# ── Core ─────────────────────────────────────────────────
from apps.core.models import ProductionLine, Machine, Shift, LineShiftAssignment
from apps.core.api.serializers import (
    ProductionLineSerializer, LineShiftAssignmentSerializer,
    MachineSerializer, ShiftSerializer,
)


class ProductionLineViewSet(viewsets.ModelViewSet):
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['code', 'name', 'product_type']


class LineShiftAssignmentViewSet(viewsets.ModelViewSet):
    queryset = LineShiftAssignment.objects.select_related('production_line', 'shift', 'supervisor')
    serializer_class = LineShiftAssignmentSerializer
    filterset_fields = ['production_line', 'is_active']


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.select_related('production_line').all()
    serializer_class = MachineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['machine_type', 'status', 'production_line']
    search_fields = ['code', 'name']


class ShiftViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


# ── Inventory ────────────────────────────────────────────
from apps.inventory.models import FiberCategory, FiberStock, DyeStock, ChemicalStock, StockTransaction
from apps.inventory.api.serializers import (
    FiberCategorySerializer, FiberStockSerializer,
    DyeStockSerializer, ChemicalStockSerializer, StockTransactionSerializer,
)


class FiberCategoryViewSet(viewsets.ModelViewSet):
    queryset = FiberCategory.objects.all()
    serializer_class = FiberCategorySerializer


class FiberStockViewSet(viewsets.ModelViewSet):
    queryset = FiberStock.objects.select_related('category')
    serializer_class = FiberStockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'quality_grade']
    search_fields = ['batch_number', 'supplier']
    ordering_fields = ['received_date', 'current_weight']


class DyeStockViewSet(viewsets.ModelViewSet):
    queryset = DyeStock.objects.all()
    serializer_class = DyeStockSerializer
    filterset_fields = ['dye_type', 'status']
    search_fields = ['name', 'color_code']


class ChemicalStockViewSet(viewsets.ModelViewSet):
    queryset = ChemicalStock.objects.all()
    serializer_class = ChemicalStockSerializer
    filterset_fields = ['chemical_type', 'status']
    search_fields = ['name']


class StockTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockTransaction.objects.all().order_by('-created_at')
    serializer_class = StockTransactionSerializer


# ── Orders ───────────────────────────────────────────────
from apps.orders.models import Customer, ColorShade, Order
from apps.orders.api.serializers import CustomerSerializer, ColorShadeSerializer, OrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['name', 'company', 'phone']


class ColorShadeViewSet(viewsets.ModelViewSet):
    queryset = ColorShade.objects.all()
    serializer_class = ColorShadeSerializer
    filterset_fields = ['is_approved']
    search_fields = ['code', 'name']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer', 'color_shade', 'production_line').order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'customer', 'production_line']
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['created_at', 'delivery_date', 'quantity_kg']


# ── Blowroom ────────────────────────────────────────────
from apps.blowroom.models import Batch as BlowroomBatch
from apps.blowroom.api.serializers import BlowroomBatchSerializer


class BlowroomBatchViewSet(viewsets.ModelViewSet):
    queryset = BlowroomBatch.objects.select_related('machine', 'operator', 'production_line').order_by('-production_date')
    serializer_class = BlowroomBatchSerializer
    filterset_fields = ['status', 'machine', 'production_date', 'production_line']
    search_fields = ['batch_number']
    ordering_fields = ['production_date']


# ── Carding ──────────────────────────────────────────────
from apps.carding.models import Production as CardingProd
from apps.carding.api.serializers import CardingProductionSerializer


class CardingProductionViewSet(viewsets.ModelViewSet):
    queryset = CardingProd.objects.select_related('machine', 'operator', 'production_line').order_by('-production_date')
    serializer_class = CardingProductionSerializer
    filterset_fields = ['status', 'machine', 'production_date', 'production_line']
    search_fields = ['batch_number']


# ── Passage ──────────────────────────────────────────────
from apps.passage.models import Production as PassageProd
from apps.passage.api.serializers import PassageProductionSerializer


class PassageProductionViewSet(viewsets.ModelViewSet):
    queryset = PassageProd.objects.select_related('machine', 'operator', 'production_line').order_by('-production_date')
    serializer_class = PassageProductionSerializer
    filterset_fields = ['status', 'machine', 'passage_number', 'production_date', 'production_line']
    search_fields = ['batch_number']


# ── Finisher ─────────────────────────────────────────────
from apps.finisher.models import Production as FinisherProd
from apps.finisher.api.serializers import FinisherProductionSerializer


class FinisherProductionViewSet(viewsets.ModelViewSet):
    queryset = FinisherProd.objects.select_related('machine', 'operator', 'production_line').order_by('-production_date')
    serializer_class = FinisherProductionSerializer
    filterset_fields = ['status', 'machine', 'production_date', 'production_line']
    search_fields = ['batch_number']


# ── Spinning ────────────────────────────────────────────
from apps.spinning.models import Production as SpinningProd, TravelerReplacement
from apps.spinning.api.serializers import SpinningProductionSerializer, TravelerReplacementSerializer


class SpinningProductionViewSet(viewsets.ModelViewSet):
    queryset = SpinningProd.objects.select_related('machine', 'operator', 'production_line').order_by('-production_date')
    serializer_class = SpinningProductionSerializer
    filterset_fields = ['status', 'machine', 'production_date', 'twist_direction', 'production_line']
    search_fields = ['batch_number', 'yarn_count']


class TravelerReplacementViewSet(viewsets.ModelViewSet):
    queryset = TravelerReplacement.objects.select_related('machine').order_by('-replaced_at')
    serializer_class = TravelerReplacementSerializer
    filterset_fields = ['machine', 'reason']


# ── Dyeing ───────────────────────────────────────────────
from apps.dyeing.models import Batch as DyeingBatch, BoilerLog, DryerLog
from apps.dyeing.api.serializers import DyeingBatchSerializer, BoilerLogSerializer, DryerLogSerializer


class DyeingBatchViewSet(viewsets.ModelViewSet):
    queryset = DyeingBatch.objects.select_related('machine', 'operator', 'color_shade', 'production_line').order_by('-production_date')
    serializer_class = DyeingBatchSerializer
    filterset_fields = ['status', 'quality_result', 'machine', 'production_date', 'production_line']
    search_fields = ['batch_number', 'color_shade__code']


class BoilerLogViewSet(viewsets.ModelViewSet):
    queryset = BoilerLog.objects.select_related('machine').order_by('-log_date')
    serializer_class = BoilerLogSerializer
    filterset_fields = ['machine', 'status', 'log_date']


class DryerLogViewSet(viewsets.ModelViewSet):
    queryset = DryerLog.objects.select_related('machine').order_by('-log_date')
    serializer_class = DryerLogSerializer
    filterset_fields = ['machine', 'status', 'log_date']


# ── Maintenance ──────────────────────────────────────────
from apps.maintenance.models import Schedule, WorkOrder, DowntimeLog, MachineServiceDate
from apps.maintenance.api.serializers import (
    ScheduleSerializer, WorkOrderSerializer,
    DowntimeLogSerializer, MachineServiceDateSerializer,
)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('machine').order_by('next_due_at')
    serializer_class = ScheduleSerializer
    filterset_fields = ['machine', 'maintenance_type', 'frequency', 'priority', 'is_active']


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.select_related('machine').order_by('-created_at')
    serializer_class = WorkOrderSerializer
    filterset_fields = ['status', 'wo_type', 'priority', 'machine']
    search_fields = ['wo_number', 'title']


class DowntimeLogViewSet(viewsets.ModelViewSet):
    queryset = DowntimeLog.objects.select_related('machine', 'shift').order_by('-start_time')
    serializer_class = DowntimeLogSerializer
    filterset_fields = ['machine', 'reason_category', 'shift']
    search_fields = ['reason_detail']


class MachineServiceDateViewSet(viewsets.ModelViewSet):
    queryset = MachineServiceDate.objects.select_related('machine').order_by('-service_date')
    serializer_class = MachineServiceDateSerializer
    filterset_fields = ['machine']


# ═══════════════════════════════════════════════════════════════
# v2.0 — تکمیل نخ (بوبین‌پیچی + دولاتابی + هیت‌ست)
# ═══════════════════════════════════════════════════════════════

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Sum, Q
from datetime import date

# ── Winding ───────────────────────────────────────────────

from apps.winding.models import Production as WindingProduction
from apps.winding.api.serializers import (
    WindingProductionSerializer, WindingProductionListSerializer
)


class WindingProductionViewSet(viewsets.ModelViewSet):
    """بوبین‌پیچی API.
    
    - GET  /api/v1/winding/           → لیست (serializer سبک)
    - GET  /api/v1/winding/{id}/      → جزئیات کامل
    - POST /api/v1/winding/           → ثبت جدید
    - GET  /api/v1/winding/kpi/       → شاخص‌های کلیدی بوبین‌پیچی
    """
    queryset = WindingProduction.objects.select_related(
        'machine', 'production_line', 'operator', 'shift', 'order'
    ).order_by('-production_date', '-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'machine', 'production_line', 'production_date', 'package_type']
    search_fields = ['batch_number']
    ordering_fields = ['production_date', 'cuts_per_100km', 'efficiency_pct', 'output_weight_kg']

    def get_serializer_class(self):
        if self.action == 'list':
            return WindingProductionListSerializer
        return WindingProductionSerializer

    @action(detail=False, methods=['get'], url_path='kpi')
    def kpi(self, request):
        """شاخص‌های کلیدی بوبین‌پیچی — با فیلتر تاریخ."""
        date_from = request.query_params.get('from', str(date.today()))
        date_to   = request.query_params.get('to',   str(date.today()))
        qs = self.queryset.filter(production_date__range=(date_from, date_to))

        agg = qs.aggregate(
            total_batches   = Count('id'),
            completed       = Count('id', filter=Q(status='completed')),
            total_output_kg = Sum('output_weight_kg'),
            total_waste_kg  = Sum('waste_weight_kg'),
            avg_cuts        = Avg('cuts_per_100km'),
            avg_efficiency  = Avg('efficiency_pct'),
        )

        # توزیع درجه کیفیت
        grade_dist = {}
        for threshold, grade in [(20, 'A'), (40, 'B'), (60, 'C'), (None, 'D')]:
            if threshold:
                count = qs.filter(cuts_per_100km__lt=threshold).exclude(
                    id__in=qs.filter(cuts_per_100km__lt=0 if threshold == 20 else [20,40,60][['A','B','C'].index(grade)-1]).values('id')
                ).count() if grade != 'A' else qs.filter(cuts_per_100km__lt=20).count()
            else:
                count = qs.filter(cuts_per_100km__gte=60).count()
            grade_dist[grade] = count

        # ساده‌تر: جداگانه count به درجه
        grade_dist = {
            'A': qs.filter(cuts_per_100km__lt=20).count(),
            'B': qs.filter(cuts_per_100km__gte=20, cuts_per_100km__lt=40).count(),
            'C': qs.filter(cuts_per_100km__gte=40, cuts_per_100km__lt=60).count(),
            'D': qs.filter(cuts_per_100km__gte=60).count(),
        }

        total_in  = qs.aggregate(s=Sum('input_weight_kg'))['s'] or 0
        total_out = float(agg['total_output_kg'] or 0)
        waste_pct = round((float(agg['total_waste_kg'] or 0)) / float(total_in) * 100, 2) if total_in else None

        return Response({
            'period':       {'from': date_from, 'to': date_to},
            'total_batches': agg['total_batches'],
            'completed':    agg['completed'],
            'total_output_kg': round(total_out, 2),
            'waste_pct':    waste_pct,
            'avg_cuts_per_100km':  round(float(agg['avg_cuts']      or 0), 1),
            'avg_efficiency_pct':  round(float(agg['avg_efficiency'] or 0), 1),
            'grade_distribution': grade_dist,
        })


# ── TFO ───────────────────────────────────────────────────

from apps.tfo.models import Production as TFOProduction
from apps.tfo.api.serializers import (
    TFOProductionSerializer, TFOProductionListSerializer
)


class TFOProductionViewSet(viewsets.ModelViewSet):
    """دولاتابی TFO API.
    
    - GET  /api/v1/tfo/           → لیست
    - GET  /api/v1/tfo/{id}/      → جزئیات
    - GET  /api/v1/tfo/kpi/       → شاخص‌های کلیدی
    """
    queryset = TFOProduction.objects.select_related(
        'machine', 'production_line', 'operator', 'shift', 'order', 'winding_production'
    ).order_by('-production_date', '-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status', 'machine', 'production_line', 'production_date',
        'twist_direction', 'ply_count',
    ]
    search_fields = ['batch_number']
    ordering_fields = ['production_date', 'twist_tpm', 'breakage_count', 'efficiency_pct']

    def get_serializer_class(self):
        if self.action == 'list':
            return TFOProductionListSerializer
        return TFOProductionSerializer

    @action(detail=False, methods=['get'], url_path='kpi')
    def kpi(self, request):
        """شاخص‌های کلیدی دولاتابی."""
        date_from = request.query_params.get('from', str(date.today()))
        date_to   = request.query_params.get('to',   str(date.today()))
        qs = self.queryset.filter(production_date__range=(date_from, date_to))

        agg = qs.aggregate(
            total_batches    = Count('id'),
            completed        = Count('id', filter=Q(status='completed')),
            total_output_kg  = Sum('output_weight_kg'),
            total_waste_kg   = Sum('waste_weight_kg'),
            total_breakage   = Sum('breakage_count'),
            avg_efficiency   = Avg('efficiency_pct'),
            avg_twist        = Avg('twist_tpm'),
        )

        # توزیع جهت تاب
        twist_dist = {
            'S': qs.filter(twist_direction='S').count(),
            'Z': qs.filter(twist_direction='Z').count(),
        }

        total_in = qs.aggregate(s=Sum('input_weight_kg'))['s'] or 0
        waste_pct = None
        if total_in:
            waste_pct = round(float(agg['total_waste_kg'] or 0) / float(total_in) * 100, 2)

        return Response({
            'period':       {'from': date_from, 'to': date_to},
            'total_batches':    agg['total_batches'],
            'completed':        agg['completed'],
            'total_output_kg':  round(float(agg['total_output_kg'] or 0), 2),
            'waste_pct':        waste_pct,
            'total_breakage':   agg['total_breakage'] or 0,
            'avg_efficiency_pct': round(float(agg['avg_efficiency'] or 0), 1),
            'avg_twist_tpm':    round(float(agg['avg_twist']      or 0), 1),
            'twist_direction_distribution': twist_dist,
        })


# ── HeatSet ──────────────────────────────────────────────

from apps.heatset.models import Batch as HeatsetBatch, CycleLog
from apps.heatset.api.serializers import (
    HeatsetBatchSerializer, HeatsetBatchListSerializer, CycleLogSerializer
)


class HeatsetBatchViewSet(viewsets.ModelViewSet):
    """هیت‌ست API.
    
    - GET  /api/v1/heatset/              → لیست
    - GET  /api/v1/heatset/{id}/         → جزئیات + لاگ چرخه
    - GET  /api/v1/heatset/{id}/cycles/  → لاگ‌های دما/فشار (AI time-series)
    - GET  /api/v1/heatset/kpi/          → شاخص‌های کلیدی
    """
    queryset = HeatsetBatch.objects.select_related(
        'machine', 'production_line', 'operator', 'shift',
        'order', 'tfo_production'
    ).prefetch_related('cycle_logs').order_by('-production_date', '-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status', 'machine', 'production_line', 'production_date',
        'machine_type_hs', 'fiber_type', 'quality_result',
    ]
    search_fields = ['batch_number']
    ordering_fields = ['production_date', 'temperature_c', 'batch_weight_kg', 'shrinkage_pct']

    def get_serializer_class(self):
        if self.action == 'list':
            return HeatsetBatchListSerializer
        return HeatsetBatchSerializer

    @action(detail=True, methods=['get'], url_path='cycles')
    def cycles(self, request, pk=None):
        """لاگ‌های دما/فشار یک بچ — AI Time Series.
        
        endpoint: GET /api/v1/heatset/{id}/cycles/
        خروجی: سری زمانی دما/فشار برای رسم منحنی چرخه
        """
        batch = self.get_object()
        logs = batch.cycle_logs.order_by('log_time')
        return Response({
            'batch_id':     batch.id,
            'batch_number': batch.batch_number,
            'temperature_target': float(batch.temperature_c),
            'duration_min': batch.duration_min,
            'cycle_count':  logs.count(),
            'cycles': CycleLogSerializer(logs, many=True).data,
        })

    @action(detail=False, methods=['get'], url_path='kpi')
    def kpi(self, request):
        """شاخص‌های کلیدی هیت‌ست."""
        date_from = request.query_params.get('from', str(date.today()))
        date_to   = request.query_params.get('to',   str(date.today()))
        qs = self.queryset.filter(production_date__range=(date_from, date_to))

        agg = qs.aggregate(
            total_batches  = Count('id'),
            pass_count     = Count('id', filter=Q(quality_result='pass')),
            fail_count     = Count('id', filter=Q(quality_result='fail')),
            conditional    = Count('id', filter=Q(quality_result='conditional')),
            total_kg       = Sum('batch_weight_kg'),
            avg_temp       = Avg('temperature_c'),
            avg_shrinkage  = Avg('shrinkage_pct'),
            avg_duration   = Avg('duration_min'),
        )

        total = agg['total_batches'] or 0
        pass_rate = round(agg['pass_count'] / total * 100, 1) if total > 0 else None

        # توزیع نتیجه به نوع دستگاه
        by_machine_type = {}
        for mt in ['autoclave', 'superba', 'suessen', 'other']:
            mt_qs = qs.filter(machine_type_hs=mt)
            mt_count = mt_qs.count()
            if mt_count:
                mt_pass = mt_qs.filter(quality_result='pass').count()
                by_machine_type[mt] = {
                    'count': mt_count,
                    'pass': mt_pass,
                    'pass_rate': round(mt_pass / mt_count * 100, 1),
                }

        return Response({
            'period':          {'from': date_from, 'to': date_to},
            'total_batches':   total,
            'pass_count':      agg['pass_count'] or 0,
            'fail_count':      agg['fail_count'] or 0,
            'conditional_count': agg['conditional'] or 0,
            'pass_rate_pct':   pass_rate,
            'total_kg':        round(float(agg['total_kg'] or 0), 2),
            'avg_temperature_c': round(float(agg['avg_temp']      or 0), 1),
            'avg_shrinkage_pct': round(float(agg['avg_shrinkage'] or 0), 2),
            'avg_duration_min':  round(float(agg['avg_duration']  or 0), 1),
            'by_machine_type': by_machine_type,
        })


# ── chain endpoint ──────────────────────────────────────────

from rest_framework.views import APIView
from apps.spinning.models import Production as SpinningProduction
from apps.orders.models import Order


class ProductionChainView(APIView):
    """زنجیره کامل تولید یک سفارش.
    
    endpoint: GET /api/v1/chain/{order_id}/
    
    خروجی: همه بچ‌های SP → WD → TFO → HS مربوط به یک سفارش.
    """

    def get(self, request, order_id):
        try:
            order = Order.objects.select_related('customer').get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'سفارش یافت نشد'}, status=404)

        # بچ‌ها به ترتیب زنجیره
        spinning_qs = SpinningProduction.objects.filter(order=order).order_by('production_date')
        winding_qs  = WindingProduction.objects.filter(order=order).order_by('production_date')
        tfo_qs      = TFOProduction.objects.filter(order=order).order_by('production_date')
        heatset_qs  = HeatsetBatch.objects.filter(order=order).order_by('production_date')

        def _stage_summary(qs, weight_field, extra_fields=None):
            agg_fields = {
                'count': Count('id'),
                'completed': Count('id', filter=Q(status='completed')),
                'total_kg': Sum(weight_field),
            }
            agg = qs.aggregate(**agg_fields)
            data = {
                'count': agg['count'],
                'completed': agg['completed'],
                'total_kg': round(float(agg['total_kg'] or 0), 2),
                'batches': [
                    {
                        'id': b.id,
                        'batch_number': b.batch_number,
                        'date': str(b.production_date if hasattr(b, 'production_date') else ''),
                        'status': b.status,
                        'machine': b.machine.code,
                        'output_kg': float(getattr(b, weight_field) or 0),
                    }
                    for b in qs
                ],
            }
            return data

        # هیت‌ست فیلد وزن متفاوت است
        hs_agg = heatset_qs.aggregate(
            count=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            pass_count=Count('id', filter=Q(quality_result='pass')),
            fail_count=Count('id', filter=Q(quality_result='fail')),
            total_kg=Sum('batch_weight_kg'),
        )

        return Response({
            'order': {
                'id':           order.id,
                'order_number': order.order_number,
                'customer':     order.customer.name,
                'quantity_kg':  float(order.quantity_kg),
                'status':       order.status,
                'status_display': order.get_status_display(),
            },
            'chain': {
                'spinning': _stage_summary(spinning_qs, 'output_weight'),
                'winding':  _stage_summary(winding_qs,  'output_weight_kg'),
                'tfo':      _stage_summary(tfo_qs,      'output_weight_kg'),
                'heatset': {
                    'count':     hs_agg['count'],
                    'completed': hs_agg['completed'],
                    'pass':      hs_agg['pass_count'] or 0,
                    'fail':      hs_agg['fail_count']  or 0,
                    'total_kg':  round(float(hs_agg['total_kg'] or 0), 2),
                    'pass_rate': round(
                        (hs_agg['pass_count'] or 0) / hs_agg['count'] * 100, 1
                    ) if hs_agg['count'] else None,
                    'batches': [
                        {
                            'id': b.id,
                            'batch_number': b.batch_number,
                            'date': str(b.production_date),
                            'status': b.status,
                            'machine': b.machine.code,
                            'quality_result': b.quality_result,
                            'output_kg': float(b.batch_weight_kg),
                        }
                        for b in heatset_qs
                    ],
                },
            },
        })


# ═══════════════════════════════════════════════════════════════
# F.2 — Quality Alerts API
# endpoint: GET /api/v1/quality-alerts/
# خروجی: همه هشدارهای کیفی فعال در WD / TFO / HS
# فیلتر: ?from=YYYY-MM-DD&to=YYYY-MM-DD&level=critical|warning
# ═══════════════════════════════════════════════════════════════


class QualityAlertsView(APIView):
    """هشدارهای کیفی فعال — AI-Ready F.2.

    endpoint: GET /api/v1/quality-alerts/
    فیلترها:
      ?from=2026-01-01     → از تاریخ
      ?to=2026-02-19       → تا تاریخ
      ?level=critical      → فقط بحرانی
      ?level=warning       → فقط هشدار
      ?section=winding     → فقط بوبین‌پیچی
    """

    def get(self, request):
        today      = date.today()
        date_from  = request.query_params.get('from', str(today))
        date_to    = request.query_params.get('to',   str(today))
        level_filter   = request.query_params.get('level',   None)  # critical/warning
        section_filter = request.query_params.get('section', None)  # winding/tfo/heatset

        all_alerts = []

        # ── بوبین‌پیچی ───────────────────────────────────────────
        if not section_filter or section_filter == 'winding':
            wd_qs = WindingProduction.objects.filter(
                production_date__range=(date_from, date_to),
                metadata__has_alerts=True,
            ).select_related('machine').order_by('-production_date')
            for batch in wd_qs:
                ai_q = (batch.metadata or {}).get('ai_quality', {})
                for alert in ai_q.get('alerts', []):
                    if level_filter and alert.get('level') != level_filter:
                        continue
                    all_alerts.append({
                        'section':      'winding',
                        'section_label': 'بوبین‌پیچی',
                        'batch_id':     batch.id,
                        'batch_number': batch.batch_number,
                        'machine':      batch.machine.code,
                        'date':         str(batch.production_date),
                        'level':        alert.get('level'),
                        'code':         alert.get('code'),
                        'message':      alert.get('msg'),
                    })

        # ── دولاتابی ───────────────────────────────────────────────
        if not section_filter or section_filter == 'tfo':
            tfo_qs = TFOProduction.objects.filter(
                production_date__range=(date_from, date_to),
                metadata__has_alerts=True,
            ).select_related('machine').order_by('-production_date')
            for batch in tfo_qs:
                ai_q = (batch.metadata or {}).get('ai_quality', {})
                for alert in ai_q.get('alerts', []):
                    if level_filter and alert.get('level') != level_filter:
                        continue
                    all_alerts.append({
                        'section':      'tfo',
                        'section_label': 'دولاتابی',
                        'batch_id':     batch.id,
                        'batch_number': batch.batch_number,
                        'machine':      batch.machine.code,
                        'date':         str(batch.production_date),
                        'level':        alert.get('level'),
                        'code':         alert.get('code'),
                        'message':      alert.get('msg'),
                    })

        # ── هیت‌ست ─────────────────────────────────────────────────
        if not section_filter or section_filter == 'heatset':
            hs_qs = HeatsetBatch.objects.filter(
                production_date__range=(date_from, date_to),
                metadata__has_alerts=True,
            ).select_related('machine').order_by('-production_date')
            for batch in hs_qs:
                ai_q = (batch.metadata or {}).get('ai_quality', {})
                for alert in ai_q.get('alerts', []):
                    if level_filter and alert.get('level') != level_filter:
                        continue
                    all_alerts.append({
                        'section':      'heatset',
                        'section_label': 'هیت‌ست',
                        'batch_id':     batch.id,
                        'batch_number': batch.batch_number,
                        'machine':      batch.machine.code,
                        'date':         str(batch.production_date),
                        'level':        alert.get('level'),
                        'code':         alert.get('code'),
                        'message':      alert.get('msg'),
                    })

        # ── مرتب‌سازی و خلاصه ─────────────────────────────────
        # critical اول باشد، بعد تاریخ
        level_order = {'critical': 0, 'warning': 1}
        all_alerts.sort(key=lambda a: (level_order.get(a['level'], 9), a['date']), reverse=False)

        critical_count = sum(1 for a in all_alerts if a['level'] == 'critical')
        warning_count  = sum(1 for a in all_alerts if a['level'] == 'warning')

        return Response({
            'period':         {'from': date_from, 'to': date_to},
            'total_alerts':   len(all_alerts),
            'critical_count': critical_count,
            'warning_count':  warning_count,
            'alerts':         all_alerts,
        })
