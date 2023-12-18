from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.states.states import Support
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Command("support"))
async def support_command(message: types.Message, state: FSMContext) -> None:
    """
    Command to send message to the admin
    User always can use it
    """
    await executor.remember_message(user_id=message.from_user.id, message_id=message.message_id)
    await state.set_state(Support.message)
    await message.answer(
        text="Опишіть вашу проблему:",
    )
