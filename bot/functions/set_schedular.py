from datetime import datetime


async def set_schedular(self):
    """
    Create jobs for every user
    """
    today = datetime.now()

    for user_id in self.all_users.keys():
        await self.create_job(user_id=user_id, today=today)

    self.scheduler.start()
