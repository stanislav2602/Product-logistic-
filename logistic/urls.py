from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StockViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]