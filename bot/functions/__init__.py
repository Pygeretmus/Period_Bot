# Class for all created functions


class Executor(object):
    def __init__(self, admin, bot, scheduler, get_session):
        self.admin = admin
        self.bot = bot
        self.bot_messages = {}
        self.scheduler = scheduler
        self.__get_session = get_session

    from bot.functions.create_job import create_job
    from bot.functions.custom_round import custom_round
    from bot.functions.delete_period import delete_period
    from bot.functions.get_delay import get_delay
    from bot.functions.get_statistics import get_statistics
    from bot.functions.get_user import get_user
    from bot.functions.message_delete import message_delete
    from bot.functions.registration_cycle import registration_cycle
    from bot.functions.registration_period import registration_period
    from bot.functions.remember_message import remember_message
    from bot.functions.send_notification import send_notification
    from bot.functions.set_period import set_period
    from bot.functions.set_schedular import set_schedular

    @property
    def session(self):
        return self.__get_session()
