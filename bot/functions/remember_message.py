async def remember_message(self, user_id: int, message_id: int) -> None:
    """
    Saving unnecessary messages
    """
    self.bot_messages.setdefault(user_id, [])
    self.bot_messages[user_id].append(message_id)
