from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.states.states import Change
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Change.periods_amount)
async def change_periods_amount_state(message: types.Message, state: FSMContext) -> None:
    """
    Reacts at information change data (periods amount)

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
    user_id = message.from_user.id
    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    try:
        periods_amount = int(message.text)
        if periods_amount < 1:
            raise ValueError
        state_data = await state.update_data(periods_amount=periods_amount)
        await state.clear()

        buttons = [
            [
                types.InlineKeyboardButton(
                    text=f"ㅤ ✅ Так, все правильно!ㅤㅤ",
                    callback_data=f"create_change_{state_data['cycle_duration']}_{periods_amount}",
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text=f"ㅤ❌ Ні, дещо неправильно!",
                    callback_data=f"create_wrong_change",
                ),
            ],
        ]

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        text = f"Введено: Цикл {state_data['cycle_duration']}, Місячні {periods_amount}"

        answer = await message.answer(text=text, reply_markup=keyboard)
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
    except ValueError:
        await executor.registration_period(
            user_id=user_id, apendix="Отримані дані не є цифрами!\n", change=True
        )
