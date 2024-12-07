from django.contrib import admin
from .models import Category, Product, Signup, Cart, CartItem, Profile, Order, OrderItem

# Register models to the admin site
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Signup)
admin.site.register(Profile)

# Register the Order and OrderItem models

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'total_price', 'status', 'date_placed')
    list_filter = ('status', 'date_placed')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-date_placed',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price')
    search_fields = ('product_name',)
