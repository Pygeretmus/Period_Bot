from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.calendar_keyboard import calendar_keyboard
from bot.states.states import Registration
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Command("calendar"))
async def calendar_command(message: types.Message, state: FSMContext) -> None:
    """
    Command to open calendar
    User can't use it until he registers
    """
    await state.clear()

    user_id = message.from_user.id
    date = message.date

    await executor.message_delete(user_id=user_id)
    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    if not await executor.get_user(user_id=user_id):
        await state.set_state(Registration.cycle_duration)
        return await executor.registration_cycle(
            user_id=user_id,
            apendix="Для перегляду календаря необхідно створити профіль!\n",
        )

    await calendar_keyboard(user_id=user_id, month=date.month, year=date.year)
