from datetime import date, timedelta


async def get_statistics(
    self, user_id: int, next_month: int, next_month_year: int
) -> tuple[list[date], list[date], list[date]]:
    """
    Statistics that returns a list of dates for creating a calendar and analytics
    """
    user = await self.get_user(user_id=user_id)

    first_menstruation = user.first_menstruation

    if user.default_periods_amount:
        periods_amount = user.default_periods_amount
    else:
        periods_amount = await self.custom_round(user.periods_amount / user.cycle_amount)
    if user.default_cycle_duration:
        cycle_duration = user.default_cycle_duration
    else:
        cycle_duration = await self.custom_round(user.cycle_duration / user.cycle_amount)

    ovulation, pregnant_average, period = [], [], []

    # Create statistics only until next month
    end_date = date(month=next_month, year=next_month_year, day=1)

    while first_menstruation < end_date:

        for period_day in range(periods_amount):
            period.append(first_menstruation + timedelta(days=period_day))

        for pregnant_average_day in range(10, 17):
            if pregnant_average_day == 13:  # Ovulation day
                ovulation.append(first_menstruation + timedelta(days=pregnant_average_day))
            else:
                pregnant_average.append(first_menstruation + timedelta(days=pregnant_average_day))

        first_menstruation += timedelta(days=cycle_duration)  # update cycle
    return ovulation, pregnant_average, period
