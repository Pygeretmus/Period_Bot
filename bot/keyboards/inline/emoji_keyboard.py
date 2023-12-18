from aiogram import types
from aiogram.enums import ParseMode

from loader import executor


async def emoji_keyboard(user_id: int, message_id: int = False) -> None:
    """
    Creating emoji menu
    '''
    Your emoji
    ┌-----------------┐
    |    Main menu    |
    └-----------------┘
    '''
    """
    user = await executor.get_user(user_id=user_id)
    emoji = user.emojis[0]

    text = (
        "Ваші емодзі зараз:\n"
        f"1) Місячні {emoji.period}\n"
        f"2) Підтвердження місячних {emoji.confirmed_period}\n"
        f"3) Середній шанс завагітніти {emoji.pregnant_average}\n"
        f"4) Овуляція {emoji.ovulation}\n"
        f"5) Незахищений секс {emoji.unprotected_sex}\n"
        f"6) Захищений секс {emoji.protected_sex}\n"
        f"7) Сильне бажання {emoji.desire}\n"
        f"8) Мастурбація {emoji.masturbation}\n"
        "Для того, щоб змінити емодзі напишіть:\n"
        "<code>Емодзі 1)_, 4)_</code>\n"
        "Наприклад: Емодзі 1)🩸, 4)🟥"
    )

    button = [
        [
            types.InlineKeyboardButton(
                text=f"📋 Повернутися в головне меню", callback_data=f"menu_open"
            )
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)

    # Change message
    if message_id:
        await executor.bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
    # Or send new
    else:
        answer = await executor.bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
        await executor.message_delete(user_id=user_id)
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
