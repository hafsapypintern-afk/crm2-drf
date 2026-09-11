from django.db.models import Q, F, Sum, Count

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Customer
from products.models import Product
from orders.models import Order

from .serializers import (
    DashboardCustomerSerializer,
    DashboardProductSerializer,
    DashboardOrderSerializer,
    DashboardOrderWithItemsSerializer,
    HighestAmountOrderSerializer,
    FrequentCustomerSerializer,
)


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        customer_count = Customer.customers.count()

        product_count = Product.objects.count()

        order_count = Order.objects.count()

        recent_customers = (
            Customer.customers
            .order_by("-created_at")[:5]
        )

        filtered_customers = (
            Customer.customers
            .filter(
                Q(city__iexact="Lahore") |
                Q(city__iexact="Islamabad")
            )
        )

        recent_orders = (
            Order.objects.select_related("customer").order_by("-order_date")[:5])

        recent_orders_with_items = (
            Order.objects
            .select_related("customer")
            .prefetch_related("items__product")
            .order_by("-order_date")[:5]
        )

        low_stock_products = (Product.objects.filter(stock__lt=5).order_by("stock"))

        highest_amount_orders = (
            Order.objects.annotate(total_amount=Sum(
                    F("items__quantity") *
                    F("items__unit_price")
                )
            ).order_by("-total_amount")[:5]
        )

        frequent_customers = (Customer.customers.annotate(order_count=Count("orders"))
            .order_by("-order_count")[:5])

        return Response({
            "summary": {
                "customer_count": customer_count,
                "product_count": product_count,
                "order_count": order_count,
            },

            "recent_customers":
                DashboardCustomerSerializer(recent_customers,many=True).data,

            "filtered_customers":
                DashboardCustomerSerializer(filtered_customers,many=True).data,

            "recent_orders":
                DashboardOrderSerializer(recent_orders,many=True).data,

            "recent_orders_with_items":
                DashboardOrderWithItemsSerializer(recent_orders_with_items,many=True).data,

            "low_stock_products":
                DashboardProductSerializer(
                    low_stock_products,
                    many=True
                ).data,

            "highest_amount_orders":
                HighestAmountOrderSerializer(
                    highest_amount_orders,
                    many=True
                ).data,

            "frequent_customers":
                FrequentCustomerSerializer(
                    frequent_customers,
                    many=True
                ).data,
        })