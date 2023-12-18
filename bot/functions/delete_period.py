from datetime import date, timedelta

from bot.models.models import Period


async def delete_period(self, user_id: int, date: date) -> None:
    """
    Deleting period from database
    """
    user = await self.get_user(user_id=user_id)

    confirmed_period = [period.date for period in user.periods]

    first_menstruation = user.first_menstruation
    days_difference = (date - first_menstruation).days

    tomorrow = date + timedelta(days=1)

    # Last period in database -> you can't remove last period in database
    if len(confirmed_period) == 1:
        answer = await self.bot.send_message(
            chat_id=user_id,
            text=(
                "Ви не можете видалити останній місячний!\nАле ви можете видалити профіль - /reset"
            ),
        )
        await self.remember_message(user_id=user_id, message_id=answer.message_id)

    # Period before current cycle start -> you can't remove periods from a cycle that has already passed
    elif days_difference < 0:
        answer = await self.bot.send_message(
            chat_id=user_id,
            text=(
                "Ви не можете видаляти місячні з циклу, що же пройшов. Актуальний цикл розпочався"
                f" {first_menstruation.day}.{first_menstruation.month}.{first_menstruation.year}"
            ),
        )
        await self.remember_message(user_id=user_id, message_id=answer.message_id)

    elif days_difference >= 0:
        save = True

        # Period not first and not last -> you can't remove periods between other periods
        if days_difference > 0 and tomorrow in confirmed_period:
            answer = await self.bot.send_message(
                chat_id=user_id,
                text="Ви не можете видаляти підтвердження місячних між іншими місячними!",
            )
            await self.remember_message(user_id=user_id, message_id=answer.message_id)
        else:
            # We shouldn't change data if it has been recently changed
            if user.cycle_amount > 1:
                # Period first in current cycle -> you can remove it
                if days_difference == 0:

                    # If we have another period of this cycle
                    if tomorrow in confirmed_period:
                        user.cycle_duration += 1  # Just add to last cycle duration 1 day
                        user.first_menstruation = tomorrow  # And change last cycle start date

                    # If we don't have another period of current cycle we need to return our statistics back
                    else:
                        confirmed_period.remove(date)  # 'Delete' period from confirmed periods
                        new_first_menstruation = max(confirmed_period)  # Find date of last period
                        count = 1  # Confirmed periods from last cycle counter
                        while True:  # Let's find start of the last period
                            yesterday = new_first_menstruation - timedelta(days=1)
                            if yesterday in confirmed_period:
                                new_first_menstruation = yesterday
                                count += 1
                            else:
                                break

                        # Now we can undo current cycle creation
                        user.periods_amount -= count
                        user.first_menstruation = new_first_menstruation
                        user.cycle_amount -= 1
                        user.cycle_duration -= (date - new_first_menstruation).days

            # Now we can change database
            self.session.delete(
                self.session.query(Period)
                .filter(Period.person_id == user.id, Period.date == date)
                .first()
            )
            self.session.commit()
