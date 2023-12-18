from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.states.states import Change
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Change.cycle_duration)
async def change_cycle_duration_state(message: types.Message, state: FSMContext) -> None:
    """
    Reacts at information change data (cycle duration)
    """
    user_id = message.from_user.id
    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    try:
        cycle_duration = int(message.text)
        if cycle_duration < 1:
            raise ValueError
        await state.update_data(cycle_duration=cycle_duration)
        await state.set_state(Change.periods_amount)
        await executor.registration_period(user_id=user_id, change=True)
    except ValueError:
        await executor.registration_cycle(
            user_id=user_id, apendix="Отримані дані не є цифрами!\n", change=True
        )
