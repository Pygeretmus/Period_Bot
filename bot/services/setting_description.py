from aiogram import Bot


async def set_default_description(bot: Bot) -> None:
    """
    Set description which user can see at first launch
    """
    description = (
        "У цьому боті ви можете слідкувати за власним циклом.\n"
        "Для початку роботи натисніть кнопку 'РОЗПОЧАТИ' або введіть команду /start.\n"
        "Для отримання детального опису введіть команду /help."
    )
    await bot.set_my_description(description=description)
