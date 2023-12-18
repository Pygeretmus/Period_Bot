from datetime import date

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.registration_calendar_keyboard import registration_calendar_keyboard
from bot.states.states import Registration
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.callback_query(F.data.startswith("registration_"))
async def registration_first_menstruation_state(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """
    Reacts at registration data (first menstruation date)
    '''
    Are you sure?
    ┌-----------------┐
    |       Yes       |
    └-----------------┘
    ┌-----------------┐
    |        No       |
    └-----------------┘
    '''
    """
    user_id = callback.from_user.id
    message_id = callback.message.message_id

    if await state.get_state() != Registration.first_menstruation:
        answer = await callback.message.answer(
            text=(
                "В даний момент я не очікував від тебе даних з календарю!\n"
                "Якщо щось зламалось передай розробнику через команду /support"
            )
        )
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
        return

    data = callback.data.split("_")
    action = data[1]

    if action == "show":
        await registration_calendar_keyboard(
            user_id=int(user_id),
            month=int(data[2]),
            year=int(data[3]),
            message_id=int(message_id),
        )
    elif action == "implement":
        registration_date = date(day=int(data[2]), month=int(data[3]), year=int(data[4]))
        state_data = await state.update_data(first_menstruation=registration_date)
        await state.clear()
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=f"ㅤ ✅ Так, все правильно!ㅤㅤ",
                    callback_data=f"create_registration_{state_data['cycle_duration']}_{state_data['periods_amount']}_{registration_date}",
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text=f"ㅤ❌ Ні, дещо неправильно!",
                    callback_data=f"create_wrong_none",
                ),
            ],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        text = (
            f"Введено: Цикл {state_data['cycle_duration']}, "
            f"Місячні {state_data['periods_amount']}, "
            f"Початок циклу {registration_date.strftime('%d.%m.%Y')}"
        )
        answer = await callback.message.answer(text=text, reply_markup=keyboard)
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
