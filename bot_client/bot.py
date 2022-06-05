from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from asgiref.sync import sync_to_async
from bot_client import keyboards, utils
from bot_admin.models import *
from bot_admin.management.bot_creator import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink
from bot_client.json_func import Data
from config.settings import CHANNEL_ID


# ------------------------------------- REGISTRATION OF USERS -------------------------------------------

class Reg_User(StatesGroup):
    name = State()
    city = State()
    phone_number = State()


# Catching 1 response from client to reg: user_id, user_name, name_lastname
# @dp.message_handler(content_types=['text'], state=Reg_User.name)
async def reg_name(message: types.Message, state: FSMContext):
    defaults = {'name': message.text}
    await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)
    await Reg_User.next()
    city_name = await message.answer("Откуда Вы ? 📍", reply_markup=keyboards.reg_place)
    async with state.proxy() as data:
        data['city_name'] = city_name.message_id


# Catching 2 response from client to reg: city
# @dp.message_handler(content_types=['text'], state=Reg_User.city)
async def reg_city(message: types.Message, state: FSMContext):
    contact = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    defaults = {'region': message.text}
    await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id, message_id=data['city_name'])
        del data['city_name']
        await Reg_User.next()
        tel_num = await message.answer("Пожалуйста введите или отправьте свой номер телефона ☎️",
                                       reply_markup=contact.
                                       add(KeyboardButton("Поделиться контактом 📞", request_contact=True)))
        data['tel_num'] = tel_num.message_id


# Final Catching 3 response from client to reg: phone_number
# @dp.message_handler(content_types=['contact', 'text'], state=Reg_User.phone_number)
async def reg_number(message: types.Message, state: FSMContext):
    if "contact" in message:
        defaults = {'number': message.contact.phone_number}
        await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)
    else:
        defaults = {'number': message.text}
        await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)

    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id, message_id=data['tel_num'])
        del data['tel_num']
    await state.finish()
    await message.answer("Регистрация прошла успешно ! 🥳😃\nСпасибо, что уделили ваше время!")
    await start_menu(message, state=state)


# -----------------------------------------------------------------------------------------------------


# ------------------------------------- BUILDING MINING FARM -------------------------------------------

class Build_Mining(StatesGroup):
    motherboard = State()
    cpu = State()
    gpu = State()
    ssd = State()
    ram = State()
    cooler = State()
    power_unit = State()


# Exit from "state" of State Machine
# @dp.callback_query_handler(lambda callback: callback.data.startswith("cancel_building"), state="*")
async def cancel_building(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    chat_id = callback.message.chat.id
    if current_state is None:
        pass
    else:
        if callback.data == "cancel_building":
            await state.finish()
            await utils.delete_mining_order_or_products(callback=callback, user_id=chat_id)
            await callback.message.delete()
            await keyboards.main_menu(message=callback.message)
            await callback.answer("Сборка майнинг фермы отменена !", show_alert=True)
        elif callback.data == "cancel_building|home":
            await state.finish()
            await utils.delete_mining_order_or_products(callback=callback, user_id=chat_id)
            await callback.message.delete()
            await keyboards.main_menu(message=callback.message)
            await callback.answer("Сборка майнинг фермы отменена !", show_alert=True)


# Catching 1 response from client to build_farm: choosing motherboard
# @dp.callback_query_handler(lambda callback: callback.data, state=Build_Mining.motherboard)
async def choose_motherboard(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands_list = await utils.get_mining_brands(callback=callback, current_state=current_state)
    products_list = await utils.get_mining_products(callback=callback, pci_number="", brand_name="", current_state=current_state)
    print("This is choosing motherboard state")
    if callback.data == "choose_motherboard":
        await callback.message.delete()
        await keyboards.pci_numbers(callback=callback, state=state)
        await callback.answer()
    elif callback.data.isdigit():
        async with state.proxy() as data:
            data['pci_number'] = callback.data
        await callback.message.delete()
        await keyboards.get_mining_brands(callback=callback, state=state)
        await callback.answer()
    elif callback.data in brands_list:
        await callback.message.delete()
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=callback.data, pci_number=data['pci_number'], state=state)
        await callback.answer()
    elif callback.data in products_list:
        await callback.message.delete()
        await mining_product_info(callback=callback, state=state)

    elif callback.data.startswith("next_page"):
        print("nexttt")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        print("prevvv")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith('collect'):
        await callback.message.delete()
        await collect(callback=callback, state=state)
        await Build_Mining.next()

        text = "Выберите ПРОЦЕССОР  👇"
        building_buttons = InlineKeyboardMarkup(row_width=2)
        building_buttons.add(InlineKeyboardButton("Выбрать процессор", callback_data="choose_cpu"),
                             InlineKeyboardButton("Отменить сборку", callback_data="cancel_building"))
        await callback.message.answer(text, reply_markup=building_buttons)
        await callback.answer()

    elif callback.data.startswith("prev"):
        await callback.message.delete()
        if callback.data.split(sep='|')[-1] == "to_pci_numbers":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['pci_numbers_text'], reply_markup=data['pci_numbers'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_brands":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_brands_text'],
                                       reply_markup=data['get_mining_brands'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_products":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_products_text'],
                                       reply_markup=data['get_mining_products'])
        await callback.answer()


# Catching 2 response from client to build_farm: choosing cpu
# @dp.callback_query_handler(lambda callback: callback.data, state=Build_Mining.cpu)
async def choose_cpu(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands_list = await utils.get_mining_brands(callback=callback, current_state=current_state)
    products_list = await utils.get_mining_products(callback=callback, pci_number="", brand_name="", current_state=current_state)
    if callback.data == "choose_cpu":
        await callback.message.delete()
        await keyboards.get_mining_brands(callback=callback, state=state)
        await callback.answer()
    elif callback.data in brands_list:
        await callback.message.delete()
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=callback.data, pci_number=data['pci_number'], state=state)
        await callback.answer()
    elif callback.data in products_list:
        await callback.message.delete()
        await mining_product_info(callback=callback, state=state)

    elif callback.data.startswith("next_page"):
        print("nexttt")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        print("prevvv")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith('collect'):
        await callback.message.delete()
        await collect(callback=callback, state=state)
        await Build_Mining.next()

        text = "Выберите ВИДЕОКАРТУ  👇"
        building_buttons = InlineKeyboardMarkup(row_width=2)
        building_buttons.add(InlineKeyboardButton("Выбрать видеокарту", callback_data="choose_gpu"),
                             InlineKeyboardButton("Отменить сборку", callback_data="cancel_building"))
        await callback.message.answer(text, reply_markup=building_buttons)
        await callback.answer()

    elif callback.data.startswith("prev"):
        await callback.message.delete()
        if callback.data.split(sep='|')[-1] == "to_get_mining_brands":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_brands_text'],
                                       reply_markup=data['get_mining_brands'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_products":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_products_text'],
                                       reply_markup=data['get_mining_products'])
        await callback.answer()


# Catching 3 response from client to build_farm: choosing gpu
# @dp.callback_query_handler(lambda callback: callback.data, state=Build_Mining.gpu)
async def choose_gpu(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands_list = await utils.get_mining_brands(callback=callback, current_state=current_state)
    products_list = await utils.get_mining_products(callback=callback, pci_number="", brand_name="", current_state=current_state)
    if callback.data == "choose_gpu":
        await callback.message.delete()
        await keyboards.get_mining_brands(callback=callback, state=state)
        await callback.answer()
    elif callback.data in brands_list:
        await callback.message.delete()
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=callback.data, pci_number=data['pci_number'], state=state)
        await callback.answer()
    elif callback.data in products_list:
        await callback.message.delete()
        await mining_product_info(callback=callback, state=state)

    elif callback.data.startswith("next_page"):
        print("nexttt")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        print("prevvv")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith('collect'):
        await callback.message.delete()
        await collect(callback=callback, state=state)
        await Build_Mining.next()

        text = "Выберите SSD диск  👇"
        building_buttons = InlineKeyboardMarkup(row_width=2)
        building_buttons.add(InlineKeyboardButton("Выбрать SSD", callback_data="choose_ssd"),
                             InlineKeyboardButton("Отменить сборку", callback_data="cancel_building"))
        await callback.message.answer(text, reply_markup=building_buttons)
        await callback.answer()

    elif callback.data.startswith("prev"):
        await callback.message.delete()
        if callback.data.split(sep='|')[-1] == "to_get_mining_brands":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_brands_text'],
                                       reply_markup=data['get_mining_brands'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_products":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_products_text'],
                                       reply_markup=data['get_mining_products'])
        await callback.answer()


# Catching 4 response from client to build_farm: choosing ssd
# @dp.callback_query_handler(lambda callback: callback.data, state=Build_Mining.ssd)
async def choose_ssd(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands_list = await utils.get_mining_brands(callback=callback, current_state=current_state)
    products_list = await utils.get_mining_products(callback=callback, pci_number="", brand_name="", current_state=current_state)
    if callback.data == "choose_ssd":
        await callback.message.delete()
        await keyboards.get_mining_brands(callback=callback, state=state)
        await callback.answer()
    elif callback.data in brands_list:
        await callback.message.delete()
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=callback.data, pci_number=data['pci_number'], state=state)
        await callback.answer()
    elif callback.data in products_list:
        await callback.message.delete()
        await mining_product_info(callback=callback, state=state)

    elif callback.data.startswith("next_page"):
        print("nexttt")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        print("prevvv")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith('collect'):
        await callback.message.delete()
        await collect(callback=callback, state=state)
        await Build_Mining.next()

        text = "Выберите ОЗУ  👇"
        building_buttons = InlineKeyboardMarkup(row_width=2)
        building_buttons.add(InlineKeyboardButton("Выбрать ОЗУ", callback_data="choose_ram"),
                             InlineKeyboardButton("Отменить сборку", callback_data="cancel_building"))
        await callback.message.answer(text, reply_markup=building_buttons)
        await callback.answer()

    elif callback.data.startswith("prev"):
        await callback.message.delete()
        if callback.data.split(sep='|')[-1] == "to_get_mining_brands":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_brands_text'],
                                       reply_markup=data['get_mining_brands'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_products":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_products_text'],
                                       reply_markup=data['get_mining_products'])
        await callback.answer()


# Catching 5 response from client to build_farm: choosing ram
# @dp.callback_query_handler(lambda callback: callback.data, state=Build_Mining.ram)
async def choose_ram(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands_list = await utils.get_mining_brands(callback=callback, current_state=current_state)
    products_list = await utils.get_mining_products(callback=callback, pci_number="", brand_name="", current_state=current_state)
    if callback.data == "choose_ram":
        await callback.message.delete()
        await keyboards.get_mining_brands(callback=callback, state=state)
        await callback.answer()
    elif callback.data in brands_list:
        await callback.message.delete()
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=callback.data, pci_number=data['pci_number'], state=state)
        await callback.answer()
    elif callback.data in products_list:
        await callback.message.delete()
        await mining_product_info(callback=callback, state=state)

    elif callback.data.startswith("next_page"):
        print("nexttt")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        print("prevvv")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith('collect'):
        await callback.message.delete()
        await collect(callback=callback, state=state)
        await Build_Mining.next()

        text = "Выберите Кулер для материнской платы  👇"
        building_buttons = InlineKeyboardMarkup(row_width=2)
        building_buttons.add(InlineKeyboardButton("Выбрать Кулер", callback_data="choose_cooler"),
                             InlineKeyboardButton("Отменить сборку", callback_data="cancel_building"))
        await callback.message.answer(text, reply_markup=building_buttons)
        await callback.answer()

    elif callback.data.startswith("prev"):
        await callback.message.delete()
        if callback.data.split(sep='|')[-1] == "to_get_mining_brands":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_brands_text'],
                                       reply_markup=data['get_mining_brands'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_products":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_products_text'],
                                       reply_markup=data['get_mining_products'])
        await callback.answer()


# Catching 6 response from client to build_farm: choosing cooler
# @dp.callback_query_handler(lambda callback: callback.data, state=Build_Mining.cooler)
async def choose_cooler(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands_list = await utils.get_mining_brands(callback=callback, current_state=current_state)
    products_list = await utils.get_mining_products(callback=callback, pci_number="", brand_name="", current_state=current_state)
    if callback.data == "choose_cooler":
        await callback.message.delete()
        await keyboards.get_mining_brands(callback=callback, state=state)
        await callback.answer()
    elif callback.data in brands_list:
        await callback.message.delete()
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=callback.data, pci_number=data['pci_number'], state=state)
        await callback.answer()
    elif callback.data in products_list:
        await callback.message.delete()
        await mining_product_info(callback=callback, state=state)

    elif callback.data.startswith("next_page"):
        print("nexttt")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        print("prevvv")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith('collect'):
        await callback.message.delete()
        await collect(callback=callback, state=state)
        await Build_Mining.next()

        text = "Выберите Блок питания  👇"
        building_buttons = InlineKeyboardMarkup(row_width=2)
        building_buttons.add(InlineKeyboardButton("Выбрать блок питания", callback_data="choose_power_unit"),
                             InlineKeyboardButton("Отменить сборку", callback_data="cancel_building"))
        await callback.message.answer(text, reply_markup=building_buttons)
        await callback.answer()

    elif callback.data.startswith("prev"):
        await callback.message.delete()
        if callback.data.split(sep='|')[-1] == "to_get_mining_brands":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_brands_text'],
                                       reply_markup=data['get_mining_brands'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_products":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_products_text'],
                                       reply_markup=data['get_mining_products'])
        await callback.answer()


# Catching 7 response from client to build_farm: choosing power_unit
# @dp.callback_query_handler(lambda callback: callback.data, state=Build_Mining.power_unit)
async def choose_power_unit(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    current_state = await state.get_state()
    brands_list = await utils.get_mining_brands(callback=callback, current_state=current_state)
    products_list = await utils.get_mining_products(callback=callback, pci_number="", brand_name="", current_state=current_state)
    if callback.data == "choose_power_unit":
        await callback.message.delete()
        await keyboards.get_mining_brands(callback=callback, state=state)
        await callback.answer()
    elif callback.data in brands_list:
        await callback.message.delete()
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=callback.data, pci_number=data['pci_number'], state=state)
        await callback.answer()
    elif callback.data in products_list:
        await callback.message.delete()
        await mining_product_info(callback=callback, state=state)

    elif callback.data.startswith("next_page"):
        print("nexttt")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        print("prevvv")
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        async with state.proxy() as data:
            await keyboards.get_mining_products(callback=callback, brand_name=brand_name,
                                                pci_number=data['pci_number'], state=state)
        await callback.answer()

    elif callback.data.startswith('collect'):
        await callback.message.delete()
        await collect(callback=callback, state=state)
        await state.finish()

        text = "Ваша майнинг ферма готова  ⚒💰💎  \nПерейдите в МОЮ ФЕРМУ  ⚙️📦 и оформите заказ  ✅ 👇"
        building_buttons = InlineKeyboardMarkup(row_width=2)
        building_buttons.add(InlineKeyboardButton("МОЯ ФЕРМА  ⚙️📦", callback_data="my_farm"),
                             InlineKeyboardButton("Главное меню  🏠", callback_data="home"))
        await callback.message.answer(text, reply_markup=building_buttons)
        await callback.answer()

    elif callback.data.startswith("prev"):
        await callback.message.delete()
        if callback.data.split(sep='|')[-1] == "to_get_mining_brands":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_brands_text'],
                                       reply_markup=data['get_mining_brands'])
        elif callback.data.split(sep='|')[-1] == "to_get_mining_products":
            async with state.proxy() as data:
                await bot.send_message(chat_id=chat_id, text=data['get_mining_products_text'],
                                       reply_markup=data['get_mining_products'])
        await callback.answer()


# -------------------------------------- MAIN MENU --------------------------------------------------

# @dp.message_handler(commands=['start'])
async def start_menu(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.chat.id
    user = await utils.check_user(user_id=chat_id)
    if user:
        await keyboards.main_menu(message=message)
    else:
        print("Created new object in Client model")
        await sync_to_async(Client.objects.create, thread_sensitive=True)(user_id=chat_id)
        await message.answer("Мы рады вас видеть вас в нашем боте ! 😊\n"
                             "Уделите немного времени для регистрации вашего аккаунта в боте!")
        await Reg_User.name.set()
        await message.answer("Введите своё имя  👤 :")


# ------------------------------------ CALLBACK QUERY HANDLER ---------------------------------------------

async def product_info(callback):
    chat_id = callback.message.chat.id
    product_name = callback.data
    product_path = f"products={product_name}/"
    data = await Data(user_id=chat_id, path=product_path)
    data.create_path()
    details_list = await utils.get_product_details(product_name=product_name)
    photo = InputFile(details_list[0])
    product_name = details_list[1]
    description = details_list[2]
    price = str(details_list[3])
    caption = f"<strong>{product_name}</strong>\n\n{description}\n\n{price} $"

    product_actions = InlineKeyboardMarkup(row_width=2)
    go_to_cart = InlineKeyboardButton('Перейти в корзину 🛒', callback_data="go_to_cart")
    adding = InlineKeyboardButton("Добавить в корзину 📥", callback_data=f"add_to_cart|{product_name}")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    prev = InlineKeyboardButton("Назад  ↩️", callback_data="prev")
    product_actions.add(go_to_cart, adding, home, prev)
    await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=product_actions)


async def mining_product_info(callback, state):
    chat_id = callback.message.chat.id
    product_name = callback.data
    current_state = await state.get_state()
    details_list = await utils.get_mining_product_details(product_name=product_name, current_state=current_state)
    photo = InputFile(details_list[0])
    product_name = details_list[1]
    description = details_list[2]
    price = str(details_list[3])
    caption = f"<strong>{product_name}</strong>\n\n{description}\n\n{price} $"

    product_actions = InlineKeyboardMarkup(row_width=2)
    adding = InlineKeyboardButton("Добавить в Мою Ферму 📥", callback_data=f"collect|{product_name}")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="cancel_building|home")
    prev = InlineKeyboardButton("Назад  ↩️", callback_data="prev|to_get_mining_products")
    product_actions.add(adding)
    product_actions.row(home, prev)
    await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=product_actions)


async def collect(callback, state):
    chat_id = callback.message.chat.id
    product_name = callback.data.split(sep='|')[-1]
    current_state = await state.get_state()
    details_list = await utils.get_mining_product_details(product_name=product_name, current_state=current_state)
    total_check = 0
    product_quantity = 1
    product_name = details_list[1]
    product_price = details_list[3]
    order = await utils.check_order(user_id=chat_id)
    if order:
        product_in_cart = await utils.check_mining_product_in_cart(user_id=chat_id)
        print("Order in cart")
        if product_name in product_in_cart:
            print('Product in cart')
            await callback.answer(text="Вы уже добавили данный товар в Мою Ферму 📥", show_alert=True)
        else:
            print("Product is not in cart")
            total_sum = product_quantity * product_price
            await utils.add_mining_product_to_cart(user_id=chat_id, product_name=product_name,
                                                   product_quantity=product_quantity, product_price=product_price,
                                                   total_sum=total_sum, current_state=current_state)
            await callback.answer(text="Товар добавлен в Мою Ферму 📥", show_alert=True)
    else:
        print("Order is not in cart")
        await utils.add_order(user_id=chat_id, total_check=total_check)
        product_in_cart = await utils.check_mining_product_in_cart(user_id=chat_id)
        if product_name in product_in_cart:
            print('Product in cart')
            await callback.answer(text="Вы уже добавили данный товар в Мою Ферму 📥", show_alert=True)
        else:
            print("Product is not in cart")
            total_sum = product_quantity * product_price
            await utils.add_mining_product_to_cart(user_id=chat_id, product_name=product_name,
                                                   product_quantity=product_quantity, product_price=product_price,
                                                   total_sum=total_sum, current_state=current_state)
            await callback.answer(text="Товар добавлен в Мою Ферму 📥", show_alert=True)


async def to_basket(box, callback):
    chat_id = callback.message.chat.id
    cart_products = await utils.cart_products_details(box=box, callback=callback, user_id=chat_id)
    print(type(cart_products), cart_products, len(cart_products))
    if len(cart_products) > 0:
        await callback.message.delete()
        basket_buttons = InlineKeyboardMarkup(row_width=4)
        order_list = ''
        total_check = 0
        for i in range(len(cart_products)):
            total_check += cart_products[i][3]
            order_list += f"{i + 1})  <strong>{cart_products[i][0]}</strong> :  " \
                          f"{cart_products[i][1]} x {cart_products[i][2]} $ = {cart_products[i][3]} $\n"
            if i == len(cart_products) - 1:
                order_list += f"\n\nИтого :  {total_check} $\n\nОплата производится в национальной валюте.\n" \
                              f"Принимаются все виды оплат: Click/Payme, Наличные, Перечисление и т.д." \
                              f"\n\nToʻlov milliy valyutada amalga oshiriladi.\n" \
                              f"Barcha toʻlov turlari qabul qilinadi: Click/Payme, Naqd pul, Pul oʻtkazish va h.k."

        for i in range(len(cart_products)):
            basket_buttons.insert(InlineKeyboardButton("➖", callback_data=f"minus|{box}|{cart_products[i][0]}")). \
                insert(InlineKeyboardButton(f"{cart_products[i][1]}", callback_data="quantity")). \
                insert(InlineKeyboardButton("➕", callback_data=f"plus|{box}|{cart_products[i][0]}")). \
                insert(InlineKeyboardButton(f"❌  {cart_products[i][0]}", callback_data=f"remove|{box}|{cart_products[i][0]}"))
        basket_buttons.add(InlineKeyboardButton("🗑  Очистить корзину", callback_data=f"clean|{box}"),
                           InlineKeyboardButton("🔍  Продолжить покупку", callback_data=f"home"))
        basket_buttons.row(InlineKeyboardButton("✅  Оформить покупку", callback_data=f"order|{box}"))
        if box == "go_to_cart":
            await bot.send_message(chat_id, "Ваша корзина   🛒 :\n\n" + order_list, reply_markup=basket_buttons)
        elif box == "my_farm":
            await bot.send_message(chat_id, "Ваша майнинг ферма  ⚙️📦 :\n\n" + order_list, reply_markup=basket_buttons)
        await callback.answer()

    else:
        print("0 items")
        if box == "go_to_cart":
            await callback.answer(text="Ваша корзина пуста  🗑", show_alert=True)
        elif box == "my_farm":
            await callback.answer(text="Ваша майнинг ферма пуста  🗑", show_alert=True)


# @dp.callback_query_handler(lambda callback: callback.data)
async def command_response(callback: types.CallbackQuery, state: FSMContext):
    categories_list = await utils.get_all_categories()
    subcategories_list = await utils.get_all_subcategories()
    brands_list = await utils.get_all_brands()
    products_list = await utils.get_all_products()
    chat_id = callback.message.chat.id

    if callback.data == "catalog":
        await callback.message.delete()
        await keyboards.categories(callback=callback)
        await callback.answer()

    elif callback.data in categories_list:
        print("Showed category_content")
        await callback.message.delete()
        category_name = callback.data
        await keyboards.subcategories_or_brands(callback=callback, category_name=category_name)
        await callback.answer()

    elif callback.data in subcategories_list:
        print("Showed subcategory_content")
        await callback.message.delete()
        brand_name = callback.data
        await keyboards.subcategory_brands(callback=callback, subcategory_name=brand_name)
        await callback.answer()

    elif callback.data in brands_list:
        print("Showed brand_content")
        await callback.message.delete()
        brand_name = callback.data
        await keyboards.brand_products(callback=callback, brand_name=brand_name)
        await callback.answer()

    elif callback.data.startswith("next_page"):
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        await keyboards.brand_products(callback=callback, brand_name=brand_name)
        await callback.answer()

    elif callback.data.startswith("prev_page"):
        await callback.message.delete()
        brand_name = callback.data.split(sep='|')[-1]
        await keyboards.brand_products(callback=callback, brand_name=brand_name)
        await callback.answer()

    elif callback.data in products_list:
        await callback.message.delete()
        await product_info(callback=callback)
        await callback.answer()

    elif callback.data == "home":
        await callback.message.delete()
        await start_menu(message=callback.message, state=state)

    elif callback.data == "prev":
        await callback.message.delete()
        product_path = ""
        json_path = await Data(user_id=chat_id, path=product_path)
        path = json_path.get_path()
        print(type(path), "Current path : ", path)
        last_room = path.split(sep='/')[-2]
        prev_room = path.split(sep='/')[-3]
        print("Last room in path : ", last_room)
        print("Prev room in path : ", prev_room)

        if "products" in last_room:
            brand_name = prev_room.split(sep='=')[-1]
            await keyboards.brand_products(callback=callback, brand_name=brand_name)
            json_path.delete()
            await callback.answer()

        elif "brands" in last_room:
            if "subcategories" in prev_room:
                subcategory_name = prev_room.split(sep='=')[-1]
                await keyboards.subcategory_brands(callback=callback, subcategory_name=subcategory_name)
            else:
                category_name = prev_room.split(sep='=')[-1]
                await keyboards.subcategories_or_brands(callback=callback, category_name=category_name)
            json_path.delete()
            await callback.answer()

        elif "subcategories" in last_room:
            category_name = prev_room.split(sep='=')[-1]
            await keyboards.subcategories_or_brands(callback=callback, category_name=category_name)
            json_path.delete()
            await callback.answer()

        elif "categories" in last_room:
            await keyboards.categories(callback=callback)
            json_path.delete()
            await callback.answer()

    elif callback.data.startswith("add_to_cart"):
        product_name = callback.data.split(sep='|')[-1]
        details_list = await utils.get_product_details(product_name=product_name)
        total_check = 0
        product_quantity = 1
        product_name = details_list[1]
        product_price = details_list[3]
        order = await utils.check_order(user_id=chat_id)
        if order:
            product_in_cart = await utils.check_product_in_cart(user_id=chat_id)
            print("Order in cart")
            if product_name in product_in_cart:
                print('Product in cart')
                await callback.answer(text="Вы уже добавили данный товар в корзину", show_alert=True)
            else:
                print("Product is not in cart")
                total_sum = product_quantity * product_price
                await utils.add_product_to_cart(user_id=chat_id, product_name=product_name,
                                                product_quantity=product_quantity,
                                                product_price=product_price, total_sum=total_sum)
                await callback.answer(text="Товар добавлен в корзину", show_alert=True)
        else:
            print("Order is not in cart")
            await utils.add_order(user_id=chat_id, total_check=total_check)
            product_in_cart = await utils.check_product_in_cart(user_id=chat_id)
            if product_name in product_in_cart:
                print('Product in cart')
                await callback.answer(text="Вы уже добавили данный товар в корзину", show_alert=True)
            else:
                print("Product is not in cart")
                total_sum = product_quantity * product_price
                await utils.add_product_to_cart(user_id=chat_id, product_name=product_name,
                                                product_quantity=product_quantity,
                                                product_price=product_price, total_sum=total_sum)
                await callback.answer(text="Товар добавлен в корзину", show_alert=True)

    elif callback.data == "go_to_cart":
        box = callback.data
        await to_basket(box=box, callback=callback)

    elif callback.data.startswith("minus"):
        product_name = callback.data.split(sep='|')[-1]
        box = callback.data.split(sep='|')[1]
        product_details = await utils.cart_product_detail(box=box, user_id=chat_id, product_name=product_name)
        name = product_details[0]
        quantity = product_details[1]
        price = product_details[2]
        if quantity > 1:
            quantity -= 1
        total_sum = quantity * price
        await utils.update_cart_product(box=box, user_id=chat_id, product_name=name, quantity=quantity,
                                        total_sum=total_sum)
        await to_basket(box=box, callback=callback)
        await callback.answer()

    elif callback.data.startswith("plus"):
        product_name = callback.data.split(sep='|')[-1]
        box = callback.data.split(sep='|')[1]
        product_details = await utils.cart_product_detail(box=box, user_id=chat_id, product_name=product_name)
        name = product_details[0]
        quantity = product_details[1]
        price = product_details[2]
        quantity += 1
        total_sum = quantity * price
        await utils.update_cart_product(box=box, user_id=chat_id, product_name=name, quantity=quantity,
                                        total_sum=total_sum)
        await to_basket(box=box, callback=callback)
        await callback.answer()

    elif callback.data.startswith('remove'):
        product_name = callback.data.split(sep='|')[-1]
        box = callback.data.split(sep='|')[1]
        cart_products = await utils.delete_cart_product(box=box, callback=callback, user_id=chat_id,
                                                        product_name=product_name)
        if len(cart_products) > 0:
            await to_basket(box=box, callback=callback)
        else:
            await callback.message.delete()
            await callback.answer(text="Ваша корзина пуста  🗑", show_alert=True)
            await keyboards.main_menu(message=callback.message)

    elif callback.data.startswith("clean"):
        print("Clean")
        product_name = ""
        box = callback.data.split(sep='|')[1]
        await utils.delete_cart_product(box=box, callback=callback, user_id=chat_id, product_name=product_name)
        await callback.message.delete()
        await callback.answer(text="Ваша корзина пуста  🗑", show_alert=True)
        await keyboards.main_menu(message=callback.message)

    elif callback.data.startswith("order"):
        await callback.message.delete()
        chat_id = callback.message.chat.id
        box = callback.data.split(sep='|')[1]
        cart_products = await utils.cart_products_details(box=box, callback=callback, user_id=chat_id)
        client = await utils.check_user(user_id=chat_id)
        order_list = ''
        total_check = 0
        for i in range(len(cart_products)):
            total_check += cart_products[i][3]
            order_list += f"{i + 1}) {cart_products[i][0]}\n"

        order_text = f"Поступил заказ от клиента :\nusername - {hlink('{}', 'https://t.me/{}').format(callback.message.chat.username, callback.message.chat.username)}" \
                     f"\nИмя :  {client.name} \nНомер телефона :  {client.number}." \
                     f"\n\nЗаказ на следующие товары :\n\n{order_list}"
        product_name = ""
        box = callback.data.split(sep='|')[1]
        await utils.delete_cart_product(box=box, callback=callback, user_id=chat_id, product_name=product_name)
        await utils.checkout_order(user_id=chat_id, complete=True, order_list=order_list, total_check=total_check)
        await bot.send_message(chat_id=CHANNEL_ID, text=order_text)
        await bot.send_message(chat_id=chat_id,
                               text="✅ Ваша заказ принят !\nВ скором времени с Вами свяжутся наши менеджеры 👤")

        await keyboards.main_menu(message=callback.message)
        await callback.answer()

    elif callback.data == "build_farm":
        await callback.message.delete()
        text = "Выбрать МАТЕРИНСКУЮ ПЛАТУ  👇"
        building_buttons = InlineKeyboardMarkup()
        building_buttons.add(InlineKeyboardButton("Выбрать материнскую плату", callback_data="choose_motherboard"),
                             InlineKeyboardButton("Отменть сборку", callback_data="cancel_building"))
        await callback.message.answer(text, reply_markup=building_buttons)
        order = await utils.check_order(user_id=chat_id)
        if order:
            pass
        else:
            await utils.add_order(user_id=chat_id, total_check=0)
        await Build_Mining.motherboard.set()
        await callback.answer()

    elif callback.data == "my_farm":
        box = callback.data
        await to_basket(box=box, callback=callback)

    elif callback.data == "about_us":
        await callback.message.delete()
        text_about = await utils.get_about_us()
        text = ""
        for about in text_about:
            text += about
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(row_width=1).
                               insert(InlineKeyboardButton("Главное меню  🏠", callback_data="home")))
        await callback.answer()

    elif callback.data == "contacts":
        await callback.message.delete()
        text_contacts = await utils.get_contacts()
        print(len(text_contacts))
        print(text_contacts)
        text = ""
        text_address = "<strong>Адреса :</strong>"
        text_number = "\n\n<strong>Номера телефонов :</strong>"
        text_location = "\n\n<strong>Локации адресов :</strong>"
        for i in range(len(text_contacts)):
            if i == 0 or i % 3 == 0:
                text_address += f"\n{text_contacts[i]}"
            elif i == 1 or i % 4 == 0:
                text_number += f"\n{text_contacts[i]}"
            elif i == 2 or i % 5 == 0:
                text_location += f"\n{text_contacts[i]}"

        text = text_address + text_number + text_location
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(row_width=1).
                               insert(InlineKeyboardButton("Главное меню  🏠", callback_data="home")))
        await callback.answer()


# ------------------------------------------ REGISTRATION ALL HANDLERS ---------------------------------------------


def register_client_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands=['start'], state=None)
    dp.register_message_handler(reg_name, content_types=['text'], state=Reg_User.name)
    dp.register_message_handler(reg_city, content_types=['text'], state=Reg_User.city)
    dp.register_message_handler(reg_number, content_types=['text', 'contact'], state=Reg_User.phone_number)


def register_client_callback_query_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_building, lambda callback: callback.data.startswith("cancel_building"),
                                       state="*")
    dp.register_callback_query_handler(choose_motherboard, lambda callback: callback.data,
                                       state=Build_Mining.motherboard)
    dp.register_callback_query_handler(choose_cpu, lambda callback: callback.data, state=Build_Mining.cpu)
    dp.register_callback_query_handler(choose_gpu, lambda callback: callback.data, state=Build_Mining.gpu)
    dp.register_callback_query_handler(choose_ssd, lambda callback: callback.data, state=Build_Mining.ssd)
    dp.register_callback_query_handler(choose_ram, lambda callback: callback.data, state=Build_Mining.ram)
    dp.register_callback_query_handler(choose_cooler, lambda callback: callback.data, state=Build_Mining.cooler)
    dp.register_callback_query_handler(choose_power_unit, lambda callback: callback.data, state=Build_Mining.power_unit)
    dp.register_callback_query_handler(command_response, lambda callback: callback.data)
