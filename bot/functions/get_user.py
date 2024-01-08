from typing import Literal, Union

from bot.models.models import User


async def get_user(self, user_id: int) -> Union[User, Literal[False]]:
    """
    Get user from the database
    """
    return self.session.query(User).filter(User.user_id == user_id).first()
