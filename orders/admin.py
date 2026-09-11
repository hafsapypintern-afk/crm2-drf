from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "customer",
        "order_date",
        "status",
    ]

    list_filter = [
        "status",
        "order_date",
    ]

    search_fields = [
        "customer__first_name",
        "customer__last_name",
        "customer__email",
    ]

    inlines = [
        OrderItemInline
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = [
        "order",
        "product",
        "quantity",
        "unit_price",
    ]

    list_filter = [
        "product",
    ]

    search_fields = [
        "order__customer__first_name",
        "order__customer__last_name",
        "product__product_name",
    ]