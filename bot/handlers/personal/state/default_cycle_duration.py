from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.states.states import Default
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Default.cycle_duration)
async def default_cycle_duration_state(message: types.Message, state: FSMContext) -> None:
    """
    Reacts at information default data setting (cycle duration)
    """
    user_id = message.from_user.id
    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    try:
        cycle_duration = int(message.text)
        if cycle_duration < 0:
            raise ValueError
        await state.update_data(cycle_duration=int(message.text))
        await state.set_state(Default.periods_amount)
        await executor.registration_period(
            user_id=user_id,
            change=True,
            apendix=(
                "Ти встановлюєш постійне значення!\n"
                "Для того, щоб видалити постійне значення - введи 0.\n"
            ),
        )
    except ValueError:
        await executor.registration_cycle(
            user_id=user_id,
            apendix=(
                "Ти встановлюєш постійне значення!\n"
                "Для того, щоб видалити постійне значення - введи 0.\n"
                "Отримані дані не є цифрами!\n"
            ),
            change=True,
        )
