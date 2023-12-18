from aiogram import Router, types

from loader import dp, executor

router = Router()
dp.include_router(router)


@router.message()
async def every_message(message: types.Message) -> None:
    """
    Responds to all unexpected messages
    """
    user_id = message.from_user.id
    await executor.remember_message(user_id=user_id, message_id=message.message_id)
    answer = await message.answer(
        text=(
            "В даний момент я не очікував від тебе повідомлень!\n"
            "Якщо ти хочеш щось передати розробнику, активуй команду /support"
        )
    )
    await executor.remember_message(user_id=user_id, message_id=answer.message_id)
