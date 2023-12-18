from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot) -> None:
    """
    Set all commands that you can see in menu
    """
    commands = [
        BotCommand(command="start", description="Початок взаємодії з ботом"),
        BotCommand(command="menu", description="Відкрити меню"),
        BotCommand(command="about", description="Відкрити інформацію про мене"),
        BotCommand(command="calendar", description="Відкрити календар"),
        BotCommand(command="notification", description="Показати сьогоднішнє повідомлення"),
        BotCommand(command="reset", description="Повністю видалити акаунт"),
        BotCommand(command="help", description="Показати опис команд"),
        BotCommand(command="support", description="Написати розробнику"),
    ]
    await bot.set_my_commands(commands=commands)
