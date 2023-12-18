from aiogram import Router, types
from sqlalchemy import update

from bot.keyboards.inline.emoji_keyboard import emoji_keyboard
from bot.models.models import Emoji
from bot.states.states import EmojiRequest
from loader import dp, executor

router = Router()
dp.include_router(router)

model = {
    "1": "period",
    "2": "confirmed_period",
    "3": "pregnant_average",
    "4": "ovulation",
    "5": "unprotected_sex",
    "6": "protected_sex",
    "7": "desire",
    "8": "masturbation",
}


@router.message(EmojiRequest.request)
async def emoji_state(message: types.Message) -> None:
    """
    Reacts at emoji changing message
    """
    text = message.text.lstrip("Емодзі").strip()
    user_id = message.from_user.id
    user = await executor.get_user(user_id=user_id)

    await executor.remember_message(user_id=user_id, message_id=message.message_id)

    numbers, emoji = [], []

    for example in text.split(","):
        split = example.split(")")
        numbers.append(split[0].strip())
        emoji.append(split[1].strip())
    values = {model[numbers[i]]: emoji[i] for i in range(len(numbers))}
    query = update(Emoji).where(Emoji.person_id == user.id).values(values)
    executor.session.execute(query)
    executor.session.commit()

    await executor.remember_user(user=user)
    await emoji_keyboard(user_id=user_id)
