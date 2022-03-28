import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management.base import BaseCommand
from aiogram import executor
from bot_admin.management.bot_creator import dp
from bot_client import bot


# Registering message handlers
bot.register_client_message_handlers(dp)

# Registering callback handlers
bot.register_client_callback_query_handlers(dp)


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        pass

    executor.start_polling(dp, skip_updates=True)

