from aiogram import types

from loader import executor


async def menu_keyboard(user_id: int, message_id: int = False) -> None:
    """
    Creating main menu
    '''
        Main menu
    ┌-----------------┐
    |    Profile      |
    └-----------------┘
    ┌-----------------┐
    |     Emoji       |
    └-----------------┘
    ┌-----------------┐
    |    Calendar     |
    └-----------------┘
    ┌-----------------┐
    |     Close       |
    └-----------------┘
    '''
    """
    buttons = [
        [
            types.InlineKeyboardButton(
                text=f"ㅤ  👤  Про менеㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                callback_data=f"menu_about",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤ   🎭 Змінити емодзіㅤㅤㅤㅤㅤㅤ", callback_data=f"menu_emoji"
            )
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤ📅  Подивитися мій календар",
                callback_data=f"menu_calendar",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤ ❌  Закрити менюㅤㅤㅤㅤㅤㅤ",
                callback_data=f"menu_close",
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    text = "Головне меню: "

    # Change message
    if message_id:
        await executor.bot.edit_message_text(
            chat_id=user_id, message_id=message_id, text=text, reply_markup=keyboard
        )
    # Or send new
    else:
        answer = await executor.bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=keyboard,
        )
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
