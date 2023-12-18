from datetime import date

from aiogram import F, Router, types

from bot.keyboards.inline.calendar_keyboard import calendar_keyboard
from bot.keyboards.inline.day_keyboard import day_keyboard
from loader import dp

router = Router()
dp.include_router(router)


@router.callback_query(F.data.startswith("calendar_"))
async def calendar_callback(callback: types.CallbackQuery) -> None:
    """
    Callback mostly from bot/keyboards/inline/calendar_keyboard
    """
    user_id = callback.from_user.id
    message_id = callback.message.message_id

    data = callback.data.split("_")
    action = data[1]

    if action == "week":  # Week button -> wrong button
        await callback.answer(text="Це кнопка дня тижня, вона нічого не робить!")

    elif action == "wrong":  # Empty button -> wrong button
        await callback.answer(text="Цей день в іншому місяці, зміни місяць!")

    elif action == "show":  # Change month
        await calendar_keyboard(
            user_id=user_id, month=int(data[2]), year=int(data[3]), message_id=message_id
        )

    elif action == "open":  # Show day
        await day_keyboard(
            user_id=user_id,
            date=date(
                day=int(data[2]),
                month=int(data[3]),
                year=int(data[4]),
            ),
            message_id=message_id,
        )

    await callback.answer()  # Unpress the button
