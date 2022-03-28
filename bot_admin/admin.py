from django.contrib import admin
from .models import *


# Register your models here.
class Client_Admin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'number', 'region']
    list_filter = ['region']


class Category_Admin(admin.ModelAdmin):
    list_display = ['category']


class SubCategory_Admin(admin.ModelAdmin):
    list_display = ['sub_category', 'category']
    list_filter = ['category']


class Brand_Admin(admin.ModelAdmin):
    list_display = ['brand', 'sub_category', 'category']
    list_filter = ['sub_category', 'category']


class Product_Admin(admin.ModelAdmin):
    list_display = ['name', 'sub_category', 'category']
    list_filter = ['category', 'sub_category', 'brand']


class Order_Admin(admin.ModelAdmin):
    list_display = ['pk', 'client', 'order_items', 'total_check', 'complete', 'date_ordered']
    list_filter = ['client']


class OrderItem_Admin(admin.ModelAdmin):
    list_display = ['client_id', 'order_id', 'product', 'product_quantity', 'product_price', 'total_sum', 'date_added']
    list_filter = ['client_id']


class Contact_Admin(admin.ModelAdmin):
    list_display = ['addresses', 'phone_numbers', 'locations']


class AboutUs_Admin(admin.ModelAdmin):
    list_display = ['about_us']


admin.site.register(Client, Client_Admin)
admin.site.register(Category, Category_Admin)
admin.site.register(SubCategory, SubCategory_Admin)
admin.site.register(Brand, Brand_Admin)
admin.site.register(Product, Product_Admin)
admin.site.register(Order, Order_Admin)
admin.site.register(OrderItem, OrderItem_Admin)
admin.site.register(Contact, Contact_Admin)
admin.site.register(About_Us, AboutUs_Admin)

