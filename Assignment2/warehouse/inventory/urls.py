# Assignment2/warehouse/inventory/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, PurchaseViewSet, PurchaseDetailViewSet, SellViewSet, SellDetailViewSet, ItemListView, stock_report

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'purchase', PurchaseViewSet)
router.register(r'sell', SellViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('purchase/<str:header_code>/details/', PurchaseDetailViewSet.as_view({'get': 'list'}), name='purchase-detail'),
    path('sell/<str:header_code>/details/', SellDetailViewSet.as_view({'get': 'list'}), name='sell-detail'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('purchase/', PurchaseViewSet.as_view({'get': 'list', 'post': 'create'}), name='purchase-list'),
    path('sell/', SellViewSet.as_view({'get': 'list', 'post': 'create'}), name='sell-list'),
    path('stock_report/<str:item_code>/', stock_report, name='stock-report'),  
]