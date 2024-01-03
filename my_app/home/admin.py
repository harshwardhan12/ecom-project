from django.contrib import admin
from .models import Customer, Product
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display=('name', 'mobile',)
    
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('name', 'price', 'description',)
    
admin.site.register(Product, ProductAdmin)

        