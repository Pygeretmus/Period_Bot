from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter


async def set_default_name(bot: Bot) -> None:
    """
    Set bot name
    """
    # You can't change bot name using this command more than 1 time in a day
    try:
        await bot.set_my_name(name="PeriodBot")
    except TelegramRetryAfter:
        pass
