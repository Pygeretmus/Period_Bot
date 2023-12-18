async def registration_period(self, user_id, apendix="", change=False) -> None:
    """
    Sending message for registration or change purposes
    """
    if change:
        apendix += "Ти намагаєшься змінити свої персональні дані!\n"

    answer = await self.bot.send_message(
        chat_id=user_id,
        text=apendix + "Введи середню кількість місячних за один цикл:",
    )
    await self.remember_message(user_id=user_id, message_id=answer.message_id)
