from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, String, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    first_menstruation = Column(Date)  # beginning of the nearest cycle
    cycle_duration = Column(Integer)  # total duration of all cycles
    periods_amount = Column(Integer)  # total number of all periods
    cycle_amount = Column(Integer, default=1)  # number of tracking cycles
    default_cycle_duration = Column(Integer, default=0)  # cycle will have this duration
    default_periods_amount = Column(Integer, default=0)  # cycle will have this number of periods

    periods = relationship("Period", backref="user", cascade="all, delete-orphan")
    specials = relationship("SpecialDay", backref="user", cascade="all, delete-orphan")
    emojis = relationship("Emoji", backref="user", cascade="all, delete-orphan")


class Period(Base):
    __tablename__ = "period_table"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=func.current_date())
    person_id = Column(Integer, ForeignKey("user_table.id"))


class SpecialDay(Base):
    __tablename__ = "special_day_table"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    info = Column(String(length=5), default="")
    person_id = Column(Integer, ForeignKey("user_table.id"))


class Emoji(Base):
    __tablename__ = "emoji_table"
    id = Column(Integer, primary_key=True)
    period = Column(String(length=5), default="🩸")
    confirmed_period = Column(String(length=5), default="✅")
    pregnant_average = Column(String(length=5), default="🟨")
    ovulation = Column(String(length=5), default="🟥")
    unprotected_sex = Column(String(length=5), default="💘")
    protected_sex = Column(String(length=5), default="💞")
    desire = Column(String(length=5), default="🔥")
    masturbation = Column(String(length=5), default="❤️‍🔥")

    person_id = Column(Integer, ForeignKey("user_table.id"))
