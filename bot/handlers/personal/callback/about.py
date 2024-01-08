from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.reset_keyboard import reset_keyboard
from bot.states.states import Change, Default
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.callback_query(F.data.startswith("about_"))
async def about_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback from bot/keyboards/inline/about_keyboard
    """
    await state.clear()

    user_id = callback.from_user.id
    data = callback.data.split("_")
    action = data[1]

    if action == "change":  # We need to change profile information
        await state.set_state(Change.cycle_duration)
        await executor.registration_cycle(user_id=user_id, change=True)

    elif action == "default":  # We need to set default information
        await state.set_state(Default.cycle_duration)
        await executor.registration_cycle(
            user_id=user_id, change=True, apendix="Ти встановлюєш постійне значення!\n"
        )

    elif action == "reset":  # We need to delete profile
        await reset_keyboard(user_id=user_id, message_id=callback.message.message_id)

    await callback.answer()  # Unpress the button
