from django.db import transaction

from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "quantity",
            "unit_price",
        ]

        read_only_fields = [
            "id",
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "customer",
            "order_date",
            "status",
            "items",
        ]

        read_only_fields = [
            "id",
            "order_date",
        ]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(
                "An order must contain at least one item."
            )

        return items

    @transaction.atomic
    def create(self, validated_data):

        items_data = validated_data.pop("items")

        # Check all stock before changing anything
        for item_data in items_data:

            product = item_data["product"]

            quantity = item_data["quantity"]

            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"Only {product.stock} units of "
                    f"{product.product_name} are available."
                )

        order = Order.objects.create(
            **validated_data
        )

        for item_data in items_data:

            product = item_data["product"]

            quantity = item_data["quantity"]

            product.stock -= quantity

            product.save(
                update_fields=["stock"]
            )

            OrderItem.objects.create(
                order=order,
                **item_data
            )

        return order

    @transaction.atomic
    def update(self, instance, validated_data):

        items_data = validated_data.pop("items")

        # Return the stock consumed by the old order
        for old_item in instance.items.select_related(
            "product"
        ):

            product = old_item.product

            product.stock += old_item.quantity

            product.save(
                update_fields=["stock"]
            )

        # Now check whether the new order can be fulfilled
        for item_data in items_data:

            product = item_data["product"]

            quantity = item_data["quantity"]

            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"Only {product.stock} units of "
                    f"{product.product_name} are available."
                )

        # Delete old items
        instance.items.all().delete()

        # Update normal Order fields
        for field, value in validated_data.items():

            setattr(
                instance,
                field,
                value
            )

        instance.save()

        # Create new items and consume stock
        for item_data in items_data:

            product = item_data["product"]

            quantity = item_data["quantity"]

            product.stock -= quantity

            product.save(
                update_fields=["stock"]
            )

            OrderItem.objects.create(
                order=instance,
                **item_data
            )

        return instance