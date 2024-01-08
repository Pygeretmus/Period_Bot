from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from apscheduler.jobstores.base import JobLookupError

from bot.keyboards.inline.about_keyboard import about_keyboard
from bot.keyboards.inline.calendar_keyboard import calendar_keyboard
from bot.models.models import Emoji, Period, User
from bot.states.states import Change, Default, Registration
from loader import dp, executor, scheduler

router = Router()
dp.include_router(router)


@router.callback_query(F.data.startswith("create_"))
async def create_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback from registration and information change forms
    """
    await state.clear()
    user_id = callback.from_user.id
    date = callback.message.date.date()

    data = callback.data.split("_")
    action = data[1]

    # User said NO to the entered information
    if action == "wrong":
        await executor.message_delete(user_id=user_id)

        if data[2] == "change":  # Changing
            await state.set_state(Change.cycle_duration)
            await executor.registration_cycle(
                user_id=user_id, apendix="Давай спробуємо ще раз!\n", change=True
            )
        elif data[2] == "default":  # Setting default
            await state.set_state(Default.cycle_duration)
            await executor.registration_cycle(
                user_id=user_id,
                apendix=(
                    "Ти встановлюєш постійне значення!\n"
                    "Для того, щоб видалити постійне значення - введи 0.\n"
                    "Давай спробуємо ще раз!\n"
                ),
                change=True,
            )
        else:  # Registration
            await state.set_state(Registration.cycle_duration)
            await executor.registration_cycle(user_id=user_id, apendix="Давай спробуємо ще раз!\n")
        return callback.answer()  # Unpress the button

    # Delete user
    elif action == "undo":
        executor.session.delete(
            executor.session.query(User).filter(User.user_id == user_id).first()
        )
        executor.session.commit()

        try:
            scheduler.remove_job(job_id=str(user_id))
        except JobLookupError:
            pass

        await executor.message_delete(user_id=user_id)
        await callback.answer(text="Інформація видалена!")

        # New registration
        await state.set_state(Registration.cycle_duration)
        await executor.registration_cycle(user_id=user_id, apendix="Ви успішно видалили акаунт!\n")

    # User said YES to the entered information during registration
    elif action == "registration":
        periods_amount = int(data[3])
        first_menstruation = datetime.strptime(data[4], "%Y-%m-%d").date()
        today_date = datetime.now().date()
        new_user = User(
            user_id=user_id,
            cycle_duration=int(data[2]),
            periods_amount=periods_amount,
            first_menstruation=first_menstruation,
        )
        executor.session.add(new_user)
        executor.session.add(Emoji(user=new_user))

        # Creating first confirmed periods
        for days in range(periods_amount):
            menstruation_date = first_menstruation + timedelta(days=days)
            if menstruation_date <= today_date:
                executor.session.add(Period(date=menstruation_date, user=new_user))
            else:
                break
            executor.session.commit()

        await executor.message_delete(user_id=user_id)
        answer = await callback.message.answer(
            text="Тепер кожен день ви будете отримувати наступне повідомлення!"
        )
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
        await executor.send_notification(user_id=user_id, date=date)
        await executor.create_job(user_id=user_id, today=callback.message.date)
        await calendar_keyboard(user_id=user_id, month=date.month, year=date.year)
        return callback.answer(text="Операція створення профілю успішна!")

    # User said YES to the entered information during information change
    elif action == "change":
        user_for_update = await executor.get_user(user_id=user_id)
        user_for_update.cycle_duration = int(data[2])
        user_for_update.periods_amount = int(data[3])
        user_for_update.cycle_amount = 1
        executor.session.commit()

        await executor.message_delete(user_id=user_id)
        await about_keyboard(user_id=user_id, today=date)
        return callback.answer(text="Операція зміни профілю успішна!")

    elif action == "default":
        user_for_update = await executor.get_user(user_id=user_id)
        user_for_update.default_cycle_duration = int(data[2])
        user_for_update.default_periods_amount = int(data[3])
        executor.session.commit()

        await executor.message_delete(user_id=user_id)
        await about_keyboard(user_id=user_id, today=date)
        return callback.answer(text="Операція встановлення постійних значень успішна!")
