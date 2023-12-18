from typing import Literal, Union

from bot.models.models import User


async def get_user(self, user_id: int) -> Union[User, Literal[False]]:
    """
    Get cached user from internal dictionary
    """
    try:
        return self.all_users[user_id]
    except KeyError:
        return False
