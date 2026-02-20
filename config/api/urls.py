"""
Diaco MES - API Router
========================
تمام endpointها در /api/v1/
JWT: /api/v1/auth/token/ و /api/v1/auth/token/refresh/
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    # accounts + core
    UserViewSet, ProductionLineViewSet, LineShiftAssignmentViewSet,
    MachineViewSet, ShiftViewSet,
    # inventory
    FiberCategoryViewSet, FiberStockViewSet, DyeStockViewSet,
    ChemicalStockViewSet, StockTransactionViewSet,
    # orders
    CustomerViewSet, ColorShadeViewSet, OrderViewSet,
    # production
    BlowroomBatchViewSet, CardingProductionViewSet,
    PassageProductionViewSet, FinisherProductionViewSet,
    SpinningProductionViewSet, TravelerReplacementViewSet,
    # dyeing
    DyeingBatchViewSet, BoilerLogViewSet, DryerLogViewSet,
    # maintenance
    ScheduleViewSet, WorkOrderViewSet, DowntimeLogViewSet,
    MachineServiceDateViewSet,
    # v2.0 — تکمیل نخ
    WindingProductionViewSet, TFOProductionViewSet,
    HeatsetBatchViewSet, ProductionChainView,
    # v2.0 F.2 — alerts
    QualityAlertsView,
)

router = DefaultRouter()

# ── Accounts + Core ──────────────────────────────────────
router.register('users', UserViewSet, basename='user')
router.register('production-lines', ProductionLineViewSet, basename='production-line')
router.register('line-shift-assignments', LineShiftAssignmentViewSet, basename='line-shift-assignment')
router.register('machines', MachineViewSet, basename='machine')
router.register('shifts', ShiftViewSet, basename='shift')

# ── Inventory ────────────────────────────────────────────
router.register('fiber-categories', FiberCategoryViewSet, basename='fiber-category')
router.register('fiber-stocks', FiberStockViewSet, basename='fiber-stock')
router.register('dye-stocks', DyeStockViewSet, basename='dye-stock')
router.register('chemical-stocks', ChemicalStockViewSet, basename='chemical-stock')
router.register('stock-transactions', StockTransactionViewSet, basename='stock-transaction')

# ── Orders ───────────────────────────────────────────────
router.register('customers', CustomerViewSet, basename='customer')
router.register('color-shades', ColorShadeViewSet, basename='color-shade')
router.register('orders', OrderViewSet, basename='order')

# ── Production ───────────────────────────────────────────
router.register('blowroom', BlowroomBatchViewSet, basename='blowroom')
router.register('carding', CardingProductionViewSet, basename='carding')
router.register('passage', PassageProductionViewSet, basename='passage')
router.register('finisher', FinisherProductionViewSet, basename='finisher')
router.register('spinning', SpinningProductionViewSet, basename='spinning')
router.register('traveler-replacements', TravelerReplacementViewSet, basename='traveler-replacement')

# ── Dyeing ───────────────────────────────────────────────
router.register('dyeing', DyeingBatchViewSet, basename='dyeing')
router.register('boiler-logs', BoilerLogViewSet, basename='boiler-log')
router.register('dryer-logs', DryerLogViewSet, basename='dryer-log')

# ── Maintenance ───────────────────────────────────────────────
router.register('maintenance-schedules', ScheduleViewSet, basename='maintenance-schedule')
router.register('work-orders', WorkOrderViewSet, basename='work-order')
router.register('downtime-logs', DowntimeLogViewSet, basename='downtime-log')
router.register('machine-services', MachineServiceDateViewSet, basename='machine-service')

# ── v2.0 — تکمیل نخ ─────────────────────────────────────────
router.register('winding', WindingProductionViewSet, basename='winding')
router.register('tfo',     TFOProductionViewSet,     basename='tfo')
router.register('heatset', HeatsetBatchViewSet,      basename='heatset')

urlpatterns = [
    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Router
    path('', include(router.urls)),
    # v2.0 — endpoints اختصاصی
    path('chain/<int:order_id>/', ProductionChainView.as_view(), name='production-chain'),
    # v2.0 F.2 — AI Quality Alerts
    path('quality-alerts/', QualityAlertsView.as_view(), name='quality-alerts'),
]
