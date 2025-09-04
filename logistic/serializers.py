from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = StockProduct
        fields = ['product_id', 'product_title', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, source='positions.all')

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position_data in positions_data:
            StockProduct.objects.create(
                stock=stock,
                product=position_data['product'],
                quantity=position_data['quantity'],
                price=position_data['price']
            )

        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position_data in positions_data:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position_data['product'],
                defaults={
                    'quantity': position_data['quantity'],
                    'price': position_data['price']
                }
            )

        product_ids = [position_data['product'].id for position_data in positions_data]
        stock.positions.exclude(product_id__in=product_ids).delete()

        return stock