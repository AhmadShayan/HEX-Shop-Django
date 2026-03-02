from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'product_price', 'ordered')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'order_total', 'status', 'is_ordered', 'created_at')
    list_filter = ('status', 'is_ordered')
    search_fields = ('order_number', 'first_name', 'last_name', 'email')
    list_per_page = 20
    inlines = [OrderProductInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'payment_method')


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)