from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "image")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    list_editable = ("price", "is_available")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("menu_item", "item_name", "price", "quantity", "subtotal")
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "table_number", "customer_name", "total", "status")
    list_filter = ("status", "created_at", "table_number")
    search_fields = ("customer_name", "customer_phone", "id")
    list_editable = ("status",)
    readonly_fields = ("created_at", "total")
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"
