from django.contrib import admin
from .models import *


# Register your models here.
class Category_Admin(admin.ModelAdmin):
    list_display = ['mining_category']


class Brand_Admin(admin.ModelAdmin):
    list_display = ['mining_brand', 'mining_category']
    list_filter = ['mining_category']


class Motherboard_Admin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'pci_slots', 'socket_type', 'pci_express', 'ram_type']
    list_filter = ['brand', 'pci_slots', 'socket_type', 'pci_express', 'ram_type']


class CPU_Admin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price']
    list_filter = ['brand', 'socket_type']


class GPU_Admin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price']
    list_filter = ['brand', 'pci_express']


class SSD_Admin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price']
    list_filter = ['brand']


class RAM_Admin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price']
    list_filter = ['brand', 'ram_type']


class Cooler_Admin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price']
    list_filter = ['brand', 'socket_type']


class PowerUnit_Admin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price']
    list_filter = ['brand']


class MiningOrderItem_Admin(admin.ModelAdmin):
    list_display = ['pk', 'product_name', 'product_brand', 'product_category', 'product_quantity', 'product_price',
                    'total_sum', 'pci_slots', 'socket_type', 'pci_express', 'ram_type', 'date_added']
    list_filter = ['product_brand', 'product_category']


admin.site.register(Category_mining, Category_Admin)
admin.site.register(Brand_mining, Brand_Admin)
admin.site.register(Motherboard, Motherboard_Admin)
admin.site.register(CPU, CPU_Admin)
admin.site.register(GPU, GPU_Admin)
admin.site.register(SSD, SSD_Admin)
admin.site.register(RAM, RAM_Admin)
admin.site.register(Cooler, Cooler_Admin)
admin.site.register(PowerUnit, PowerUnit_Admin)
admin.site.register(Mining_OrderItem, MiningOrderItem_Admin)

