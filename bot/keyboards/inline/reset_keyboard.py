from aiogram import types

from loader import executor


async def reset_keyboard(user_id: int, message_id: int = False) -> None:
    """
    Creating reset confirmation menu
    '''
      Delete profile?
    ┌-----------------┐
    |      Yes        |
    └-----------------┘
    ┌-----------------┐
    |       No        |
    └-----------------┘
    '''
    """
    buttons = [
        [
            types.InlineKeyboardButton(
                text=f"Так, все правильно!",
                callback_data=f"create_undo",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"Ні, не треба!",
                callback_data=f"menu_about",
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    text = "🚨 Видалити всю інформацію?"

    # Change message
    if message_id:
        await executor.bot.edit_message_text(
            chat_id=user_id, message_id=message_id, text=text, reply_markup=keyboard
        )
    # Or send new
    else:
        answer = await executor.bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
