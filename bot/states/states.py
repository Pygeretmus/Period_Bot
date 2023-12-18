from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    cycle_duration = State()  # bot shows 'Введи середню тривалість циклу:'
    periods_amount = State()  # bot shows 'Введи середню кількість місячних за один цикл:'
    first_menstruation = State()  # bot shows 'Обери день початку останнього циклу'


class Change(StatesGroup):
    cycle_duration = State()  # bot shows 'Введи середню тривалість циклу (для зміни):'
    periods_amount = (State())  # bot shows 'Введи середню кількість місячних за один цикл (для зміни):'


class Default(StatesGroup):
    cycle_duration = State()  # bot shows 'Введи середню тривалість циклу (для постійного значення):'
    periods_amount = (State())  # bot shows 'Введи середню кількість місячних за один цикл (для постійного значення):'


class Support(StatesGroup):
    message = State()  # bot shows 'Опишіть вашу проблему:'


class EmojiRequest(StatesGroup):
    request = State()  # bot shows 'Для того, щоб змінити емодзі напишіть:'
