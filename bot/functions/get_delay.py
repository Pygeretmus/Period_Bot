from datetime import date, timedelta
from typing import Literal, Union


async def get_delay(self, user_id: int, today: date) -> Union[int, Literal[False]]:
    """
    Function to get how many days user period should already be
    """
    user = await self.get_user(user_id=user_id)

    if user.default_cycle_duration:
        need_to_be = user.first_menstruation + timedelta(days=user.default_cycle_duration)
    else:
        need_to_be = user.first_menstruation + timedelta(
            days=await self.custom_round(user.cycle_duration / user.cycle_amount)
        )

    delay_days = (today - need_to_be).days

    if delay_days > 0:
        return delay_days

    return False
