from datetime import date, datetime, timedelta


async def send_notification(self, user_id: id, date: date = False) -> None:
    """
    Daily notification creation

    '''
    Сьогодні (16.12):
     🟥 Овуляція (високий шанс завагітніти)
    Завтра (17.12):
     🟨 Середній шанс завагітніти
    Післязавтра (18.12):
     💃  Нічого незвичного
    '''

    """
    if not date:
        date = datetime.now().date()

    user = await self.get_user(user_id=user_id)
    emoji = user.emojis[0]

    month = date.month
    year = date.year
    next_month = month + 1 if month < 12 else 1
    next_month_year = year if month < 12 else year + 1
    today_date = date
    test_day_of_week = {0: "Сьогодні", 1: "Завтра", 2: "Післязавтра"}
    text = ""

    ovulation, pregnant_average, period = await self.get_statistics(
        user_id=user_id, next_month=next_month, next_month_year=next_month_year
    )
    delay = await self.get_delay(user_id=user_id, today=date)

    if delay:
        if str(delay)[-1] == "1":  # 1 день, 101 день, 10001 день
            text = f"Увага, затримка - {delay} день!!!\n"
        elif str(delay)[-1] in ["2", "3", "4"]:  # 2 дні, 23 дні, 404 дні
            text = f"Увага, затримка - {delay} дні!!!\n"
        else:
            text = f"Увага, затримка - {delay} днів!!!\n"  # 5 днів, 107 днів, 10 днів

    length = len(test_day_of_week.keys())  # Basically 3, but you can change test_day_of_week

    for day in range(length):
        changed = False

        day_date = today_date + timedelta(days=day)
        test_day_of_week[day] += f" ({day_date.day}.{day_date.month}):\n"

        if day_date in period:
            changed = True
            test_day_of_week[day] += f"\t{emoji.period} Місячні\n"

        if day_date in ovulation:
            changed = True
            test_day_of_week[day] += f"\t{emoji.ovulation} Овуляція (високий шанс завагітніти)\n"

        if day_date in pregnant_average:
            changed = True
            test_day_of_week[day] += f"\t{emoji.pregnant_average} Середній шанс завагітніти\n"

        if not changed:
            test_day_of_week[day] += "\t💃 Нічого незвичного\n"

        text += test_day_of_week[day]
    await self.bot.send_message(chat_id=user_id, text=text, disable_notification=True)
