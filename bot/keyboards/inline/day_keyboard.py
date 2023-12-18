from datetime import date

from aiogram import types

from bot.models.models import Period
from loader import executor


async def day_keyboard(user_id: int, date: date, message_id: int) -> None:
    """
    Creating day menu
    '''
        This day
    ┌-----------------┐       ┌-----------------┐
    | Confirm period  |   or  |   Deny period   |
    └-----------------┘       └-----------------┘
    ┌-----------------┐
    | Unprotected sex |
    └-----------------┘
    ┌-----------------┐
    |  Protected sex  |
    └-----------------┘
    ┌-----------------┐
    |     Desire      |
    └-----------------┘
    ┌-----------------┐
    |  Masturbation   |
    └-----------------┘
    ┌-----------------┐
    |  Delete marks   |
    └-----------------┘
    ┌-----------------┐
    |     Close       |
    └-----------------┘
    '''
    """
    user = await executor.get_user(user_id=user_id)
    emoji = user.emojis[0]
    specials = {str(special.date): special.info for special in user.specials}

    callback_postfix = f"{date.day}_{date.month}_{date.year}"

    emoji_meaning = {
        f"{emoji.pregnant_average}": "Середній шанс завагітніти\n",
        f"{emoji.ovulation}": "Овуляція\n",
        f"{emoji.unprotected_sex}": "Незахищений секс\n",
        f"{emoji.protected_sex}": "Захищений секс\n",
        f"{emoji.desire}": "Сильне бажання\n",
        f"{emoji.masturbation}": "Мастурбація\n",
    }

    next_month = date.month + 1 if date.month != 12 else 1
    next_month_year = date.year + 1 if date.month == 12 else date.year

    ovulation, pregnant_average, period = await executor.get_statistics(
        user_id=user_id, next_month=next_month, next_month_year=next_month_year
    )

    text = f"{date.day}.{date.month}.{date.year}\n"

    changed = False

    if date in period:
        changed = True
        text += f"\t{emoji.period} Місячні\n"

    if date in ovulation:
        changed = True
        text += f"\t{emoji.ovulation} Овуляція (високий шанс завагітніти)\n"

    if date in pregnant_average:
        changed = True
        text += f"\t{emoji.pregnant_average} Середній шанс завагітніти\n"

    if str(date) in specials:
        special_emoji = specials[f"{date}"]
        changed = True
        text += f"{special_emoji} {emoji_meaning[special_emoji]}"

    if not changed:
        text += "\t💃 Нічого незвичного\n"

    # Check period in this day
    if (
        executor.session.query(Period)
        .filter(Period.person_id == user.id, Period.date == date)
        .first()
    ):
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=f"ㅤ {emoji.period} Видалити місячні!ㅤㅤㅤㅤ",
                    callback_data=f"day_notperiod_{callback_postfix}",
                ),
            ],
        ]
    else:
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=f"ㅤㅤ{emoji.confirmed_period}  Додати місячні!ㅤㅤㅤㅤㅤㅤ",
                    callback_data=f"day_period_{callback_postfix}",
                ),
            ],
        ]

    buttons += [
        [
            types.InlineKeyboardButton(
                text=f"ㅤㅤ  {emoji.unprotected_sex}  Незахищений сексㅤㅤㅤㅤㅤ",
                callback_data=f"day_unsex_{callback_postfix}",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤㅤ  {emoji.protected_sex}  Захищений сексㅤㅤㅤㅤㅤㅤ",
                callback_data=f"day_sex_{callback_postfix}",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤㅤ  {emoji.desire}  Сильне бажанняㅤㅤㅤㅤㅤㅤ",
                callback_data=f"day_desire_{callback_postfix}",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤ   {emoji.masturbation}  Мастурбаціяㅤㅤㅤㅤㅤㅤㅤ",
                callback_data=f"day_masturbation_{callback_postfix}",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤㅤ 🚫  Ніякої особливої подіїㅤㅤㅤ",
                callback_data=f"day_nothing_{callback_postfix}",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=f"ㅤ   📅  Повернутися до календаря",
                callback_data=f"menu_calendar",
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await executor.bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboard,
    )
