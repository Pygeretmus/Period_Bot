from aiogram import exceptions


async def message_delete(self, user_id: int) -> None:
    """
    Deleting all unnecessary messages
    """
    self.bot_messages.setdefault(user_id, [])
    for message in self.bot_messages[user_id]:
        try:
            await self.bot.delete_message(chat_id=user_id, message_id=message)
        except exceptions.TelegramBadRequest:
            pass
