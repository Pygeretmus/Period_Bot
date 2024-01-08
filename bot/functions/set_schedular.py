from datetime import datetime

from bot.models.models import User


async def set_schedular(self):
    """
    Create jobs for every user
    """
    today = datetime.now()

    for user in self.session.query(User).all():
        await self.create_job(user_id=user.user_id, today=today)

    self.scheduler.start()
