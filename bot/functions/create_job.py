from datetime import datetime


async def create_job(self, user_id: int, today: datetime) -> None:
    """
    Creating a job to send daily notification
    """
    self.scheduler.add_job(
        self.send_notification,
        trigger="cron",
        start_date=today,
        hour=6,
        minute=0,
        id=str(user_id),
        kwargs={"user_id": user_id},
    )
