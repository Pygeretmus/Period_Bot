from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.calendar_keyboard import calendar_keyboard
from bot.states.states import Registration
from loader import dp, executor

router = Router()
dp.include_router(router)


@dp.message(Command("notification"))
async def notification_command(message: types.Message, state: FSMContext):
    """
    Command to send daily notification
    User can't use it until he registers
    """
    await state.clear()

    user_id = message.from_user.id

    await executor.message_delete(user_id=user_id)
    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    if not await executor.get_user(user_id=user_id):
        await state.set_state(Registration.cycle_duration)
        return await executor.registration_cycle(
            user_id=user_id,
            apendix="Для перегляду сьогоднішнього повідомлення необхідно створити профіль!\n",
        )

    await executor.send_notification(user_id=user_id, date=message.date.date())
    await calendar_keyboard(user_id=user_id, month=message.date.month, year=message.date.year)
