from datetime import date

from aiogram import types

from loader import executor


async def about_keyboard(user_id: int, today: date, message_id: id = False) -> None:
    """
    Creating profile menu
    '''
        Your profile?
    ┌-----------------┐
    |     Change      |
    └-----------------┘
    ┌-----------------┐
    |   Set default   |
    └-----------------┘
    ┌-----------------┐
    |     Delete      |
    └-----------------┘
    ┌-----------------┐
    |    Calendar     |
    └-----------------┘
    ┌-----------------┐
    |    Main menu    |
    └-----------------┘
    ┌-----------------┐
    |     Close       |
    └-----------------┘
    '''
    """
    user = await executor.get_user(user_id=user_id)
    date = user.first_menstruation

    text = (
        "Твій профіль:\nПерший день останньої менструації -"
        f" {date.day}.{date.month}.{date.year}\nСередня тривалість циклу -"
        f" {await executor.custom_round(user.cycle_duration/user.cycle_amount)}\nСередня кількість"
        " місячних -"
        f" {await executor.custom_round(user.periods_amount/user.cycle_amount)}\nКількість циклів"
        f" спостереження - {user.cycle_amount - 1}"
    )

    text += (
        f"\nВиставлена тривалість циклу - {user.default_cycle_duration}"
        if user.default_cycle_duration
        else ""
    )
    text += (
        f"\nВиставлена кількість місячних - {user.default_periods_amount}"
        if user.default_periods_amount
        else ""
    )

    delay_days = await executor.get_delay(user_id=user_id, today=today)

    if delay_days:
        text += f"\nЗатримка - {delay_days}"

    buttons = [
        [
            types.InlineKeyboardButton(
                text=f"ㅤ    🖊 Змінити статистичні даніㅤㅤㅤ",
                callback_data=f"about_change",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤ 🛠️ Встановити постійні значення",
                callback_data=f"about_default",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤ  🗑️ Видалити всю інформаціюㅤㅤ",
                callback_data=f"about_reset",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="ㅤ  📅 Відкрити календарㅤㅤㅤㅤㅤㅤ", callback_data="menu_calendar"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="ㅤㅤ   📋 Повернутися до загального меню", callback_data="menu_open"
            )
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤㅤ❌  Закрити менюㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                callback_data=f"menu_close",
            ),
        ],
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    # Change message
    if message_id:
        await executor.bot.edit_message_text(
            chat_id=user_id, message_id=message_id, text=text, reply_markup=keyboard
        )
    # Or send new
    else:
        answer = await executor.bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
