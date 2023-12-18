from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.states.states import Registration
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext) -> None:
    """
    Command to start profile creation
    User will not be able to use it until he deletes
    """
    await state.clear()

    user_id = message.from_user.id

    await executor.message_delete(user_id=user_id)
    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    if await executor.get_user(user_id=user_id):
        answer = await executor.bot.send_message(
            chat_id=user_id,
            text=(
                "Ваші дані вже існують, якщо хочете видалити їх, натисніть /reset.\n"
                "Для виклику меню натисніть /menu.\n"
                "Для навігації натисніть /help."
            ),
        )
        return await executor.remember_message(user_id=user_id, message_id=answer.message_id)

    await state.set_state(Registration.cycle_duration)
    await executor.registration_cycle(user_id=user_id)
