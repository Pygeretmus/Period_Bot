from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.states.states import Support
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message(Support.message)
async def support_state(message: types.Message, state: FSMContext) -> None:
    """
    Reacts at message to the admin
    """
    await state.clear()

    user_id = message.from_user.id

    await executor.bot.send_message(
        chat_id=executor.admin,
        text=f"Повідомлення від {user_id}:\n{message.text}",
    )
    await message.answer(text="Розробник отримав ваше повідомлення!")
