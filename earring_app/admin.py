from django.contrib import admin
from .models import  CartItem, Category,  Product,CustomerProfile,Orders
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image','category','manufacture','quantity']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(CustomerProfile)
admin.site.register(Orders)