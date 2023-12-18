from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.about_keyboard import about_keyboard
from bot.keyboards.inline.calendar_keyboard import calendar_keyboard
from bot.keyboards.inline.emoji_keyboard import emoji_keyboard
from bot.keyboards.inline.menu_keyboard import menu_keyboard
from bot.states.states import EmojiRequest
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.callback_query(F.data.startswith("menu_"))
async def menu_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Main menu callback from almost every keyboard
    """
    await state.clear()

    user_id = callback.from_user.id
    message_id = callback.message.message_id
    date = callback.message.date.date()

    data = callback.data.split("_")
    action = data[1]

    # Open main menu
    if action == "open":
        await menu_keyboard(user_id=user_id, message_id=message_id)

    # Close menu
    elif action == "close":
        await executor.message_delete(user_id=user_id)

    # Open profile menu
    elif action == "about":
        await about_keyboard(user_id=user_id, today=date, message_id=message_id)

    # Open emoji menu
    elif action == "emoji":
        await state.set_state(EmojiRequest.request)
        await emoji_keyboard(user_id=user_id, message_id=message_id)

    # Open calendar
    elif action == "calendar":
        await calendar_keyboard(
            user_id=user_id, month=date.month, year=date.year, message_id=message_id
        )
    await callback.answer()  # Unpress the button
