import os

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.functions import Executor
from bot.models.models import Base, User

load_dotenv()

# Creating database url for further connection
DATABASE_ENDPOINT = os.environ.get("DATABASE_ENDPOINT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_ENDPOINT}:"
    f"{DATABASE_PORT}/{DATABASE_NAME}"
)

# Connection to database
engine = create_engine(DATABASE_URL)

# Creating model tables in database
Base.metadata.create_all(bind=engine)

# Creating session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


async def get_session():
    return session


async def close_session():
    return session.close()


# Creating bot
bot = Bot(token=os.environ.get("TOKEN"))

# Creating dispatcher
dp = Dispatcher()

# Creating scheduler
scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
scheduler.add_job(close_session, trigger="interval", hours=4)

# Creating executor copy to use functions
executor = Executor(
    admin=os.environ.get("ADMIN"),
    bot=bot,
    get_session=get_session,
    scheduler=scheduler,
)
