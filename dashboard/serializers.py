from rest_framework import serializers

from customers.models import Customer
from products.models import Product
from orders.models import Order


class DashboardCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "city",
            "created_at",
        ]


class DashboardProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "product_price",
            "stock",
        ]


class DashboardOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.__str__",
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_name",
            "order_date",
            "status",
        ]


class DashboardOrderWithItemsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "order_date",
            "status",
            "items",
        ]

    def get_items(self, obj):
        return [
            {
                "product": item.product.id,
                "product_name": item.product.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in obj.items.all()
        ]


class HighestAmountOrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "order_date",
            "status",
            "total_amount",
        ]


class FrequentCustomerSerializer(serializers.ModelSerializer):
    order_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "order_count",
        ]