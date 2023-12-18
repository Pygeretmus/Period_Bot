import asyncio
import logging

from aiogram import Bot

from bot.models.models import Base
from bot.services.setting_commands import set_default_commands
from bot.services.setting_description import set_default_description
from bot.services.setting_name import set_default_name
from bot.services.setting_short_description import set_default_short_description
from loader import bot, dp, engine, executor


def register_all_handlers() -> None:
    """Adding all routers from bot/handlers into main dispatcher"""
    from bot import handlers

    logging.info("Handlers registered.")


async def register_all_settings(bot: Bot) -> None:
    # All commands that you can see in menu
    await set_default_commands(bot)
    logging.info("Commands registered.")
    # Bot name
    await set_default_name(bot)
    logging.info("Name set.")
    # Description at first launch
    await set_default_description(bot)
    logging.info("Description set.")
    # Description in bot profile
    await set_default_short_description(bot)
    logging.info("Short description set.")


async def init_database():
    """Connection to database and model tables creation"""
    Base.metadata.create_all(engine)
    logging.info("Database was inited")


async def on_startup(bot: Bot) -> None:
    """Bot setting up"""
    register_all_handlers()
    await init_database()
    await register_all_settings(bot)
    await executor.set_schedular()
    logging.info("Bot started.")


async def main() -> None:
    await on_startup(bot=bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")
