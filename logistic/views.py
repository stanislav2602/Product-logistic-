from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer

# Create your views here.


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['products__id']

