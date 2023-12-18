from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.registration_calendar_keyboard import registration_calendar_keyboard
from bot.states.states import Registration
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Registration.periods_amount)
async def registration_periods_amount_state(message: types.Message, state: FSMContext) -> None:
    """
    Reacts at registration data (periods amount)
    """
    user_id = message.from_user.id
    date = message.date.date()

    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    try:
        periods_amount = int(message.text)
        if periods_amount < 1:
            raise ValueError
        await state.update_data(periods_amount=periods_amount)
        await state.set_state(Registration.first_menstruation)
        await registration_calendar_keyboard(user_id=user_id, month=date.month, year=date.year)
    except ValueError:
        await executor.registration_period(user_id=user_id, apendix="Отримані дані не є цифрами!\n")
