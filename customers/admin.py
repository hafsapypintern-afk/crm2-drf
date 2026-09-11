from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "city",
        "created_at",
    ]

    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]

    list_filter = ["city", "created_at"]