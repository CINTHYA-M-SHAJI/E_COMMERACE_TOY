from django.contrib import admin

# Register your models here.
from .models import Category, Sub_Category,Age,Product,Order,OrderItem,Brand


class OrderItemTubleInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubleInline, ]
    list_display=['user','email','phone','payment_id','paid','date']
    search_fields=['email','phone','payment_id', 'date']


admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Age)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Brand)