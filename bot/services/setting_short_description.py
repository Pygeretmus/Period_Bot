from aiogram import Bot


async def set_default_short_description(bot: Bot) -> None:
    """
    Set description which user always can see in bot profile
    """
    short_description = (
        "У цьому боті ви можете слідкувати за власним циклом.\nРозробник @LiNCrYbNeS"
    )
    await bot.set_my_short_description(short_description=short_description)
