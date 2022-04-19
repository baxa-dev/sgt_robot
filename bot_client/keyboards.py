from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from bot_client import utils
from bot_admin.management.bot_creator import bot
from bot_client.json_func import Data


# REGISTRATION PLACE OF CLIENT

reg_place = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
tashkent = KeyboardButton("Город Ташкент")
andijan = KeyboardButton("Андижанская область")
buxara = KeyboardButton("Бухарская область")
fergana = KeyboardButton("Ферганская область")
djizak = KeyboardButton("Джизакская область")
khorezm = KeyboardButton("Хорезмская область")
namangan = KeyboardButton("Наманганская область")
navoiy = KeyboardButton("Навоийская область")
kashkadarya = KeyboardButton("Кашкадарьинская область")
samarkand = KeyboardButton("Самаркандская область")
sirdarya = KeyboardButton("Сырдарьинская область")
surxandarya = KeyboardButton("Сурхандарьинская область")
tashkent_region = KeyboardButton("Ташкентскаяская область")
karakalpakstan = KeyboardButton("Республика Каракалпакстан")
reg_place.row(tashkent)
reg_place.add(andijan, buxara, fergana, djizak, khorezm, namangan, navoiy, kashkadarya, samarkand, sirdarya, surxandarya, tashkent_region)
reg_place.row(karakalpakstan)


# START (MAIN) MENU
async def main_menu(message):
    text = f"Здравствуйте, <strong>{message.chat.first_name}</strong> 👋.\nДобро пожаловать в наш бот."
    keyboards = InlineKeyboardMarkup(row_width=2)
    catalog = InlineKeyboardButton("Каталог  📔🔎", callback_data="catalog")
    basket = InlineKeyboardButton("Корзина  🛒", callback_data="go_to_cart")
    build_farm = InlineKeyboardButton("СОБРАТЬ МАЙНИНГ ФЕРМУ  💰💎🛠", callback_data='build_farm')
    collection = InlineKeyboardButton("Моя ферма ⚙️📦", callback_data="my_farm")
    about_us = InlineKeyboardButton("О нас  👤", callback_data="about_us")
    contacts = InlineKeyboardButton("Контакты  ☎️📍", callback_data="contacts")
    keyboards.add(catalog)
    keyboards.row(build_farm)
    keyboards.row(basket, collection)
    keyboards.add(about_us, contacts)
    await message.answer(text, reply_markup=keyboards)


# SHOWING CATEGORIES
async def categories(callback):
    chat_id = callback.message.chat.id
    if callback.data != "prev":
        product_path = "catalog/"
        print("Showed catalog")
        data = await Data(user_id=chat_id, path=product_path)
        data.create_path()
    text = "Выберите :"
    category_buttons = InlineKeyboardMarkup(row_width=2)
    categories_list = await utils.get_all_categories()
    for category in categories_list:
        button = InlineKeyboardButton(category, callback_data=category)  # category_name
        category_buttons.insert(button)
    prev = InlineKeyboardButton("Назад  ↩️", callback_data="home")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    category_buttons.row(home)
    category_buttons.insert(prev)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=category_buttons)


# # SHOWING SUB-CATEGORIES AND PRODUCTS
# async def category_products(callback, category_name):
#     chat_id = callback.message.chat.id
#     if callback.data != "prev":
#         product_path = f"category={category_name}/"
#         data = await Data(user_id=chat_id, path=product_path)
#         data.create_path()
#     text = "Выберите :"
#     product_buttons = InlineKeyboardMarkup(row_width=2)
#     product_list = await utils.get_category_products_names(category_name=category_name)
#     for product in product_list:
#         button = InlineKeyboardButton(product, callback_data=product)
#         product_buttons.insert(button)
#     prev = InlineKeyboardButton("Назад  ↩️", callback_data=f"prev")
#     home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
#     product_buttons.row(prev)
#     product_buttons.insert(home)
#     await bot.send_message(chat_id=chat_id, text=text, reply_markup=product_buttons)


# SHOWING SUB-CATEGORIES AND PRODUCTS
async def subcategories_or_brands(callback, category_name):
    chat_id = callback.message.chat.id
    if callback.data != "prev":
        product_path = f"categories={category_name}/"
        print("Showed catalog")
        data = await Data(user_id=chat_id, path=product_path)
        data.create_path()
    text = "Выберите :"
    subcategory_and_brand_buttons = InlineKeyboardMarkup(row_width=3)
    subcategories_list = await utils.get_need_subcategories(callback=category_name)
    brands_list = await utils.get_need_brands(callback=category_name)
    for subcategory in subcategories_list:
        button = InlineKeyboardButton(subcategory, callback_data=subcategory)
        subcategory_and_brand_buttons.insert(button)

    for brand in brands_list:
        button = InlineKeyboardButton(brand, callback_data=brand)
        subcategory_and_brand_buttons.insert(button)

    prev = InlineKeyboardButton("Назад  ↩️", callback_data="prev")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    subcategory_and_brand_buttons.row(home)
    subcategory_and_brand_buttons.insert(prev)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=subcategory_and_brand_buttons)


async def subcategory_brands(callback, subcategory_name):
    chat_id = callback.message.chat.id
    text = "Выберите :"
    brand_buttons = InlineKeyboardMarkup(row_width=3)
    brands_list = await utils.get_need_subcategory_brands(callback=subcategory_name)

    if callback.data != "prev":
        product_path = f"subcategories={subcategory_name}/"
        data = await Data(user_id=chat_id, path=product_path)
        data.create_path()

    for brand in brands_list:
        button = InlineKeyboardButton(brand, callback_data=brand)
        brand_buttons.insert(button)
    prev = InlineKeyboardButton("Назад  ↩️", callback_data=f"prev")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    brand_buttons.row(home)
    brand_buttons.insert(prev)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=brand_buttons)


async def brand_products(callback, brand_name):
    chat_id = callback.message.chat.id
    text = "Выберите :"
    product_buttons = InlineKeyboardMarkup(row_width=2)
    products_list = await utils.get_need_brand_products(callback=brand_name)

    items_amount = len(products_list)

    if callback.data == "prev" or callback.data.startswith("prev_page") or callback.data.startswith("next_page"):
        pass
    else:
        product_path = f"brands={brand_name}/"
        data = await Data(user_id=chat_id, path=product_path)
        data.create_path()

    if any(map(str.isdigit, callback.data)) and "|" in callback.data:
        page_items = int(callback.data.split(sep='|')[1])
        if page_items < items_amount:
            for i in range(page_items-10, page_items):
                product = products_list[i]
                button = InlineKeyboardButton(product, callback_data=product)
                product_buttons.insert(button)
                if i != items_amount-1 and i % 10 == 9:
                    if page_items < 11:
                        next_page = InlineKeyboardButton("➡️", callback_data=f"next_page|{i + 11}|{brand_name}")
                        product_buttons.insert(next_page)
                    else:
                        prev_page = InlineKeyboardButton("⬅️", callback_data=f"prev_page|{i-9}|{brand_name}")
                        next_page = InlineKeyboardButton("➡️", callback_data=f"next_page|{i+11}|{brand_name}")
                        product_buttons.row(prev_page)
                        product_buttons.insert(next_page)
        else:
            for i in range(page_items-10, items_amount):
                product = products_list[i]
                button = InlineKeyboardButton(product, callback_data=product)
                product_buttons.insert(button)
                if i == items_amount-1:
                    last_digit = i % 10
                    prev_page = InlineKeyboardButton("⬅️", callback_data=f"prev_page|{i-last_digit}|{brand_name}")
                    product_buttons.row(prev_page)
    else:
        for i in range(items_amount):
            product = products_list[i]
            button = InlineKeyboardButton(product, callback_data=product)
            product_buttons.insert(button)
            if i != items_amount - 1 and i % 10 == 9:
                if items_amount > 10:
                    next_page = InlineKeyboardButton("➡️", callback_data=f"next_page|{i + 11}|{brand_name}")
                    product_buttons.row(next_page)
                    break

    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    prev = InlineKeyboardButton("Назад  ↩️", callback_data="prev")
    product_buttons.row(home, prev)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=product_buttons)


# ------------------------------------- MINING ACTIONS ----------------------------------------------------

async def pci_numbers(callback, state):
    chat_id = callback.message.chat.id
    slots_numbers = await utils.get_slot_numbers()
    slots_buttons = InlineKeyboardMarkup(row_width=3)
    text = "Выберите количество видеокарт, которые можно подключить к материнской плате :  ⬇️"
    for number in slots_numbers:
        button = InlineKeyboardButton(number, callback_data=number)  # number of slots
        slots_buttons.insert(button)
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="cancel_building|home")
    slots_buttons.row(home)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=slots_buttons)
    async with state.proxy() as data:
        data['pci_numbers_text'] = text
        data['pci_numbers'] = slots_buttons


async def get_mining_brands(callback, state):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands = await utils.get_mining_brands(callback=callback, current_state=current_state)
    brand_buttons = InlineKeyboardMarkup(row_width=3)
    text = "Выберите бренд :  ⬇️"
    for brand in brands:
        button = InlineKeyboardButton(brand, callback_data=brand)  # name of brands
        brand_buttons.insert(button)
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="cancel_building|home")
    if current_state == "Build_Mining:motherboard":
        prev = InlineKeyboardButton("Назад  ↩️", callback_data="prev|to_pci_numbers")
        brand_buttons.row(home, prev)
    else:
        brand_buttons.row(home)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=brand_buttons)
    async with state.proxy() as data:
        data['get_mining_brands_text'] = text
        data['get_mining_brands'] = brand_buttons


async def get_mining_products(callback, brand_name, pci_number, state):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    text = "Выберите :"
    product_buttons = InlineKeyboardMarkup(row_width=2)
    products_list = await utils.get_mining_products(pci_number=pci_number, brand_name=brand_name, current_state=current_state)

    items_amount = len(products_list)

    if any(map(str.isdigit, callback.data)) and "|" in callback.data:
        page_items = int(callback.data.split(sep='|')[1])
        if page_items < items_amount:
            for i in range(page_items - 10, page_items):
                product = products_list[i]
                button = InlineKeyboardButton(product, callback_data=product)
                product_buttons.insert(button)
                if i != items_amount - 1 and i % 10 == 9:
                    if page_items < 11:
                        next_page = InlineKeyboardButton("➡️", callback_data=f"next_page|{i + 11}|{brand_name}")
                        product_buttons.insert(next_page)
                    else:
                        prev_page = InlineKeyboardButton("⬅️", callback_data=f"prev_page|{i - 9}|{brand_name}")
                        next_page = InlineKeyboardButton("➡️", callback_data=f"next_page|{i + 11}|{brand_name}")
                        product_buttons.row(prev_page)
                        product_buttons.insert(next_page)

        else:
            for i in range(page_items-10, items_amount):
                product = products_list[i]
                button = InlineKeyboardButton(product, callback_data=product)
                product_buttons.insert(button)
                if i == items_amount-1:
                    last_digit = i % 10
                    prev_page = InlineKeyboardButton("⬅️", callback_data=f"prev_page|{i-last_digit}|{brand_name}")
                    product_buttons.row(prev_page)
    else:
        for i in range(items_amount):
            product = products_list[i]
            button = InlineKeyboardButton(product, callback_data=product)
            product_buttons.insert(button)
            if i != items_amount-1 and i % 10 == 9:
                if items_amount > 10:
                    next_page = InlineKeyboardButton("➡️", callback_data=f"next_page|{i+11}|{brand_name}")
                    product_buttons.row(next_page)
                    break

    prev = InlineKeyboardButton("Назад  ↩️", callback_data="prev|to_get_mining_brands")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    product_buttons.row(home, prev)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=product_buttons)
    async with state.proxy() as data:
        data['get_mining_products_text'] = text
        data['get_mining_products'] = product_buttons
