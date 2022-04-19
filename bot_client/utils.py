from django.template.context_processors import media
from django.db import transaction

import build_mining.models
from bot_admin.models import *
from build_mining.models import *
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from django.db.models import F
from config import settings


# ------------------------------ ACTIONS WITH USERS -------------------------------------

@sync_to_async
def create_or_update_user(user_id, defaults):
    try:
        obj = Client.objects.update_or_create(user_id=user_id, defaults=defaults)
        return obj
    except ObjectDoesNotExist:
        return None


@sync_to_async
def check_user(user_id):
    try:
        obj = Client.objects.get(user_id=user_id)
        return obj
    except ObjectDoesNotExist:
        return None


# ---------------------------- CATEGORY, SUBCATEGORY, BRAND ACTIONS ---------------------------------------

@sync_to_async
def get_all_categories():
    try:
        categories_list = []
        obj = Category.objects.all()
        for category in obj:
            categories_list.append(category.category)
        return categories_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_all_subcategories():
    try:
        subcategories_list = []
        obj = SubCategory.objects.all()
        for subcategory in obj:
            subcategories_list.append(subcategory.sub_category)
        return subcategories_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_need_subcategories(callback):
    try:
        subcategories_list = []
        obj = SubCategory.objects.filter(category__category=callback)
        for subcategory in obj:
            subcategories_list.append(subcategory.sub_category)
        return subcategories_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_all_brands():
    try:
        brands_list = []
        obj = Brand.objects.all()
        for brand_object in obj:
            brands_list.append(brand_object.brand)
        return brands_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_need_subcategory_brands(callback):
    try:
        subcategory_brands = []
        obj = Brand.objects.filter(sub_category__sub_category=callback)
        for brand_object in obj:
            subcategory_brands.append(brand_object.brand)
        return subcategory_brands
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_need_brands(callback):
    try:
        brands_list = []
        obj = Brand.objects.filter(category__category=callback)
        for brand_object in obj:
            if brand_object.sub_category is None:
                brands_list.append(brand_object.brand)
        return brands_list
    except ObjectDoesNotExist:
        return None


# -------------------------------- PRODUCTS ACTIONS ---------------------------------------


@sync_to_async
def get_all_products():
    try:
        product_list = []
        obj = Product.objects.all()
        for product in obj:
            product_list.append(product.name)
        return product_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_category_products_names(category_name):
    try:
        category_product_names = []
        obj = Product.objects.filter(category__category=category_name)
        for product in obj:
            category_product_names.append(product.name)
        print(category_product_names)
        return category_product_names
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_product_details(product_name):
    try:
        product_details = []
        obj = Product.objects.get(name=product_name)
        product_details.append(f"{settings.MEDIA_ROOT}/{obj.image}")
        product_details.append(obj.name)
        product_details.append(obj.description)
        product_details.append(obj.price)

        return product_details
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_need_brand_products(callback):
    try:
        brand_products = []
        obj = Product.objects.filter(brand__brand=callback)
        for product_object in obj:
            brand_products.append(product_object.name)
        return brand_products
    except ObjectDoesNotExist:
        return None


# ------------------------------ CART PRODUCTS ACTIONS ---------------------------------------


@sync_to_async
def check_product_in_cart(user_id):
    product_names_list = []
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        order_id = order.pk
        order_items = OrderItem.objects.filter(order_id=order_id)
        for item in order_items:
            print(type(item.product.name), item.product.name)
            product = str(item.product.name)
            print(type(product), product)
            product_names_list.append(product)
        return product_names_list
    except ObjectDoesNotExist:
        return product_names_list


@sync_to_async
def add_product_to_cart(user_id, product_name, product_quantity, product_price, total_sum):
    try:
        user = Client.objects.get(user_id=user_id)
        product = Product.objects.get(name=product_name)
        order = Order.objects.filter(client=user).get(complete=False)
        obj = OrderItem.objects.create(client_id=user, order_id=order, product=product,
                                       product_quantity=product_quantity, product_price=product_price,
                                       total_sum=total_sum)
        obj.save()
        return obj
    except ObjectDoesNotExist:
        return None


@sync_to_async
def update_cart_product(box, user_id, product_name, quantity, total_sum):
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        order_id = order.pk
        obj = []
        if box == "go_to_cart":
            product = Product.objects.get(name=product_name)
            obj = OrderItem.objects.filter(order_id=order_id).get(product__name=product)  # get
        elif box == "my_farm":
            obj = Mining_OrderItem.objects.filter(order_id=order_id).get(product_name=product_name)  # get

        obj.product_quantity = quantity
        obj.total_sum = total_sum
        obj.save()

        return obj
    except ObjectDoesNotExist:
        return None


# TRANSACTIONS
# with transaction.atomic():
        #     obj.product_quantity = quantity
        #     obj.total_sum = total_sum
        #     obj.save()


@sync_to_async
def delete_cart_product(box, callback, user_id, product_name):
    cart_products = []
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        order_id = order.pk
        products = []
        if box == "go_to_cart":
            products = OrderItem.objects.filter(order_id=order_id)
        elif box == "my_farm":
            products = Mining_OrderItem.objects.filter(order_id=order_id)

        if callback.data.split(sep='|')[0] == "clean":
            print("c")
            products.delete()

        elif callback.data.split(sep='|')[0] == "order":
            print("o")
            products.delete()

        elif callback.data.split(sep='|')[0] == "remove":
            print("r")
            if box == "go_to_cart":
                product = products.get(product__name=product_name)
                product.delete()
            elif box == "my_farm":
                product = products.get(product_name=product_name)
                product.delete()

        for item in products:
            cart_products.append(item)

        return cart_products
    except ObjectDoesNotExist:
        return cart_products


@sync_to_async
def cart_products_details(box, callback, user_id):
    all_products_details = []
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        order_id = order.pk
        order_items = []
        if box == "go_to_cart":
            order_items = OrderItem.objects.filter(order_id=order_id)
            for item in order_items:
                product_details = [str(item.product.name), item.product_quantity, item.product_price, item.total_sum]
                all_products_details.append(product_details)
        elif box == "my_farm":
            order_items = Mining_OrderItem.objects.filter(order_id=order_id)
            for item in order_items:
                product_details = [str(item.product_name), item.product_quantity, item.product_price, item.total_sum]
                all_products_details.append(product_details)

        return all_products_details
    except ObjectDoesNotExist:
        return all_products_details


@sync_to_async
def cart_product_detail(box, user_id, product_name):
    try:
        product_details = []
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        order_id = order.pk
        if box == "go_to_cart":
            # order_items = OrderItem.objects.get(product__name=product_name)
            order_items = OrderItem.objects.filter(order_id=order_id).get(product__name=product_name)
            product_details = [str(order_items.product.name), order_items.product_quantity,
                               order_items.product_price, order_items.total_sum]
        elif box == "my_farm":
            order_items = Mining_OrderItem.objects.filter(order_id=order_id).get(product_name=product_name)
            # order_items = Mining_OrderItem.objects.get(product_name=product_name)
            product_details = [str(order_items.product_name), order_items.product_quantity, order_items.product_price,
                               order_items.total_sum]
        return product_details
    except ObjectDoesNotExist:
        return None


# ---------------------------- ORDER ACTIONS ---------------------------------------


@sync_to_async
def check_order(user_id):
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        return order
    except ObjectDoesNotExist:
        return None


@sync_to_async
def add_order(user_id, total_check):
    try:
        client = Client.objects.get(user_id=user_id)
        obj = Order.objects.create(client=client, total_check=total_check, complete=False, order_items="")
        obj.save()
        return obj
    except ObjectDoesNotExist:
        return None


@sync_to_async
def checkout_order(user_id, complete, order_list, total_check):
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        order.complete = complete
        order.order_items = order_list
        order.total_check = total_check
        order.save()

        return order
    except ObjectDoesNotExist:
        return None


# ---------------------------- ABOUT_US, CONTACTS ACTIONS ---------------------------------------


@sync_to_async
def get_about_us():
    try:
        text_about = []
        obj = About_Us.objects.all()
        for text in obj:
            text_about.append(text.about_us)
        return text_about
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_contacts():
    try:
        text_contacts = []
        obj = Contact.objects.all()
        for text in obj:
            text_contacts.append(text.addresses)
            text_contacts.append(text.phone_numbers)
            text_contacts.append(text.locations)

        return text_contacts
    except ObjectDoesNotExist:
        return None


# ---------------------------- BUILD MINING ACTIONS ---------------------------------------

@sync_to_async
def get_slot_numbers():
    try:
        numbers = set()
        slots = Motherboard.objects.all().order_by('pci_slots')
        for slot in slots:
            numbers.add(slot.pci_slots)

        return numbers
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_mining_brands(callback, current_state):
    try:
        brands_list = set()
        chat_id = callback.message.chat.id
        obj = []
        order = Order.objects.filter(client__user_id=chat_id).get(complete=False)
        order_id = order.pk
        if current_state == "Build_Mining:motherboard":
            obj = Motherboard.objects.all()
            if callback.data.isdigit():
                obj = obj.filter(pci_slots=int(callback.data))
        elif current_state == "Build_Mining:cpu":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            socket_type = motherboard.socket_type
            obj = CPU.objects.filter(socket_type__socket_type=socket_type)
        elif current_state == "Build_Mining:gpu":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            pci_express = motherboard.pci_express.replace(" ", "")
            pci_express = pci_express.split(sep=',')
            gpu = GPU.objects.all()
            for item in gpu:
                pci = item.pci_express.all()
                for ver in pci:
                    versions = list(ver.pci_express)
                    # if versions in pci_express:
                    if (True for i in versions if i in pci_express):
                        print("version")
                        obj = item
                brands_list.add(obj.brand.mining_brand)
            obj = []

        elif current_state == "Build_Mining:ssd":
            obj = SSD.objects.all()
        elif current_state == "Build_Mining:ram":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            ram_type = motherboard.ram_type
            obj = RAM.objects.filter(ram_type__ram_type=ram_type)
        elif current_state == "Build_Mining:cooler":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            socket_type = motherboard.socket_type
            obj = Cooler.objects.filter(socket_type__socket_type=socket_type)
        elif current_state == "Build_Mining:power_unit":
            obj = PowerUnit.objects.all()
        for brand_object in obj:
            brands_list.add(brand_object.brand.mining_brand)
        return brands_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_mining_products(pci_number, brand_name, current_state):
    try:
        products_list = []
        obj = ""
        if current_state == "Build_Mining:motherboard":
            obj = Motherboard.objects.all()
        elif current_state == "Build_Mining:cpu":
            obj = CPU.objects.all()
        elif current_state == "Build_Mining:gpu":
            obj = GPU.objects.all()
        elif current_state == "Build_Mining:ssd":
            obj = SSD.objects.all()
        elif current_state == "Build_Mining:ram":
            obj = RAM.objects.all()
        elif current_state == "Build_Mining:cooler":
            obj = Cooler.objects.all()
        elif current_state == "Build_Mining:power_unit":
            obj = PowerUnit.objects.all()

        if brand_name == "":
            for brand_object in obj:
                products_list.append(brand_object.name)
        else:
            obj = obj.filter(brand__mining_brand=brand_name)
            obj = obj.filter(pci_slots=pci_number)
            for brand_object in obj:
                products_list.append(brand_object.name)
        return products_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_mining_product_details(product_name, current_state):
    try:
        product_details = []
        obj = ""
        if current_state == "Build_Mining:motherboard":
            obj = Motherboard.objects.get(name=product_name)
        elif current_state == "Build_Mining:cpu":
            obj = CPU.objects.get(name=product_name)
        elif current_state == "Build_Mining:gpu":
            obj = GPU.objects.get(name=product_name)
        elif current_state == "Build_Mining:ssd":
            obj = SSD.objects.get(name=product_name)
        elif current_state == "Build_Mining:ram":
            obj = RAM.objects.get(name=product_name)
        elif current_state == "Build_Mining:cooler":
            obj = Cooler.objects.get(name=product_name)
        elif current_state == "Build_Mining:power_unit":
            obj = PowerUnit.objects.get(name=product_name)

        product_details.append(f"{settings.MEDIA_ROOT}/{obj.image}")
        product_details.append(obj.name)
        product_details.append(obj.description)
        product_details.append(obj.price)

        return product_details
    except ObjectDoesNotExist:
        return None


@sync_to_async
def check_mining_product_in_cart(user_id):
    product_names_list = []
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        order_id = order.pk
        order_items = Mining_OrderItem.objects.filter(order_id=order_id)
        for item in order_items:
            print(type(item.product_name), item.product_name)
            product = str(item.product_name)
            print(type(product), product)
            product_names_list.append(product)
        return product_names_list
    except ObjectDoesNotExist:
        return product_names_list


@sync_to_async
def add_mining_product_to_cart(user_id, product_name, product_quantity, product_price, total_sum, current_state):
    try:
        user = Client.objects.get(user_id=user_id)
        order = Order.objects.filter(client=user).get(complete=False)
        product = ""
        pci_slots = 0
        socket_type = ""
        ram_type = ""
        pci_express = ""

        order_id = order.pk

        if current_state == "Build_Mining:motherboard":
            product = Motherboard.objects.get(name=product_name)
            pci_slots = product.pci_slots
            socket_type = product.socket_type
            pci_express = product.pci_express
            ram_type = product.ram_type
        elif current_state == "Build_Mining:cpu":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            product = CPU.objects.get(name=product_name)
            socket_type = motherboard.socket_type
        elif current_state == "Build_Mining:gpu":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            product = GPU.objects.get(name=product_name)
            pci_express = motherboard.pci_express
        elif current_state == "Build_Mining:ssd":
            product = SSD.objects.get(name=product_name)
        elif current_state == "Build_Mining:ram":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            product = RAM.objects.get(name=product_name)
            ram_type = motherboard.ram_type
        elif current_state == "Build_Mining:cooler":
            motherboard = Mining_OrderItem.objects.filter(order_id=order_id).first()
            product = Cooler.objects.get(name=product_name)
            socket_type = motherboard.socket_type
        elif current_state == "Build_Mining:power_unit":
            product = PowerUnit.objects.get(name=product_name)

        product_brand = product.brand.mining_brand
        product_category = product.category.mining_category

        obj = Mining_OrderItem.objects.create(client_id=user, order_id=order, product_name=product_name,
                                              product_quantity=product_quantity, product_price=product_price,
                                              total_sum=total_sum, product_brand=product_brand,
                                              product_category=product_category, pci_slots=pci_slots,
                                              socket_type=socket_type, pci_express=pci_express, ram_type=ram_type)
        obj.save()
        return obj
    except ObjectDoesNotExist:
        return None


@sync_to_async
def delete_mining_order_or_products(callback, user_id):
    try:
        order = Order.objects.filter(client__user_id=user_id).get(complete=False)
        if callback.data == "cancel_building":
            order.delete()
        elif callback.data == "cancel_building|home":
            order.delete()

    except ObjectDoesNotExist:
        return None
