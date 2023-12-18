from datetime import date

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import delete, update

from bot.keyboards.inline.calendar_keyboard import calendar_keyboard
from bot.models.models import SpecialDay
from loader import dp, executor

router = Router()
dp.include_router(router)


@router.callback_query(F.data.startswith("day_"))
async def day_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Callback from bot/keyboards/inline/day_keyboard
    """
    await state.clear()

    user_id = callback.from_user.id
    user = await executor.get_user(user_id=user_id)
    emoji = user.emojis[0]

    data = callback.data.split("_")
    action = data[1]
    set_date = date(day=int(data[2]), month=int(data[3]), year=int(data[4]))

    # Period confirmation
    if action == "period":
        await executor.set_period(user_id=user_id, date=set_date)

    # Period denial
    elif action == "notperiod":
        await executor.delete_period(user_id=user_id, date=set_date)

    # Adding some special marks
    else:
        special_day = (
            executor.session.query(SpecialDay)
            .filter(SpecialDay.person_id == user_id, SpecialDay.date == set_date)
            .first()
        )

        if not special_day:
            special_day = SpecialDay(user=user, date=set_date)
            executor.session.add(special_day)
            executor.session.commit()

        if action == "unsex":
            query = (
                update(SpecialDay)
                .where(SpecialDay.person_id == user.id, SpecialDay.date == set_date)
                .values({"info": emoji.unprotected_sex})
            )

        elif action == "sex":
            query = (
                update(SpecialDay)
                .where(SpecialDay.person_id == user.id, SpecialDay.date == set_date)
                .values({"info": emoji.protected_sex})
            )

        elif action == "desire":
            query = (
                update(SpecialDay)
                .where(SpecialDay.person_id == user.id, SpecialDay.date == set_date)
                .values({"info": emoji.desire})
            )

        elif action == "masturbation":
            query = (
                update(SpecialDay)
                .where(SpecialDay.person_id == user.id, SpecialDay.date == set_date)
                .values({"info": emoji.masturbation})
            )

        elif action == "nothing":
            query = delete(SpecialDay).where(
                SpecialDay.person_id == user.id, SpecialDay.date == set_date
            )

        executor.session.execute(query)
        executor.session.commit()

    await calendar_keyboard(
        user_id=user_id,
        month=set_date.month,
        year=set_date.year,
        message_id=callback.message.message_id,
    )
    await callback.answer()  # Unpress the button
