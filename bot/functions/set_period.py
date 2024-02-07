from datetime import timedelta

from bot.models.models import Period


async def set_period(self, user_id, date: int = False) -> None:
    """
    Saving period in database
    """
    user = await self.get_user(user_id=user_id)

    confirmed_period = [period.date for period in user.periods]
    first_menstruation = user.first_menstruation
    days_difference = (date - first_menstruation).days

    # Day before the start of the current cycle -> you can't add periods to a cycle that has already passed
    if days_difference < -1:
        answer = await self.bot.send_message(
            chat_id=user_id,
            text=(
                "Ви не можете додавати місячні до циклу, що вже пройшов. Актуальний цикл розпочався"
                f" {first_menstruation.day}.{first_menstruation.month}.{first_menstruation.year}"
            ),
        )
        await self.remember_message(user_id=user_id, message_id=answer.message_id)

    # Day before the start of the current cycle -> you can add period
    elif days_difference == -1:
        self.session.add(Period(date=date, user=user))  # lets add period
        user.first_menstruation = date  # change current cycle start date
        user.cycle_duration -= 1  # and reduce last cycle duration by 1 day
        self.session.commit()

    else:
        self.session.add(Period(user=user, date=date))

        # If this period not next in cycle -> we have started new cycle
        if date - timedelta(days=1) not in confirmed_period:
            user.cycle_duration += days_difference
            # Lets find all confirmed periods since last cycle
            last_cycle = [
                period_date for period_date in confirmed_period if period_date >= first_menstruation
            ]
            user.periods_amount += len(last_cycle)  # and add them to statistics
            user.cycle_amount += 1  # increase the number of tracked cycles by 1
            user.first_menstruation = date  # and set current cycle first day
        self.session.commit()
