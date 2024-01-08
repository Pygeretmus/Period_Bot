import calendar
from datetime import datetime

from aiogram import types
from aiogram.enums import ParseMode

from loader import executor

day_of_the_week = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]

months_name = {
    1: "Січень",
    2: "Лютий",
    3: "Березень",
    4: "Квітень",
    5: "Травень",
    6: "Червень",
    7: "Липень",
    8: "Серпень",
    9: "Вересень",
    10: "Жовтень",
    11: "Листопад",
    12: "Грудень",
}


async def registration_calendar_keyboard(
    user_id: int, month: int, year: int, message_id: int = 0
) -> None:
    """
    Similar to calendar_keyboard but with registration callbacks
    '''
                Chose current cycle start date:

    ┌---------------------------------------------------------┐
    |                    <<Previous month<<                   |
    └---------------------------------------------------------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Monday  |     |         |     |   11    |     |   25    |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Tuesday |     |         |     |   12    |     |   26    |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    |Wednesday|     |         |     |   13    |     |   27    |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    |Thursday |     |         |     |   14    |     |   28    |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Friday  |     |    1    |     |   15    |     |   29    |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    |Saturday |     |    2    |     |   16    |     |   30    |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Sunday  |     |    3    |     |  |17|   |     |   31    |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Monday  |     |    4    |     |   18    |     |         |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Tuesday |     |    5    |     |   19    |     |         |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    |Wednesday|     |    6    |     |   20    |     |         |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    |Thursday |     |    7    |     |   21    |     |         |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Friday  |     |    8    |     |   22    |     |         |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    |Saturday |     |    9    |     |   23    |     |         |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------┐     ┌---------┐     ┌---------┐     ┌---------┐
    | Sunday  |     |   10    |     |   24    |     |         |
    └---------┘     └---------┘     └---------┘     └---------┘
    ┌---------------------------------------------------------┐
    |                      >>Next month>>                     |
    └---------------------------------------------------------┘
    ┌---------------------------------------------------------┐
    |                        Main menu                        |
    └---------------------------------------------------------┘
    ┌---------------------------------------------------------┐
    |                          Close                          |
    └---------------------------------------------------------┘
    '''
    """
    now = datetime.now()

    today = False

    # If we in current year and month
    if month == now.month and year == now.year:
        today = now.day

    previous_month = month - 1 if month != 1 else 12
    previous_month_year = year if month != 1 else year - 1

    next_month = month + 1 if month != 12 else 1
    next_month_year = year + 1 if month == 12 else year

    # Creating list of days [0, 0, 0, 0, 1, 2, 3, 4, 5,6 ... 28, 29, 30, 31]
    my_calendar = [day for week in calendar.monthcalendar(year=year, month=month) for day in week]
    length = len(my_calendar)

    # We need 14 * 3 columns, or 14*2 columns if we have Monday - 1st February
    if length == 35:
        my_calendar += [0] * 7
        length += 7

    buttons = [
        [
            types.InlineKeyboardButton(
                text=f"<<{months_name[previous_month]}<<",
                callback_data=f"registration_show_{previous_month}_{previous_month_year}",
            ),
        ]
    ]

    # To create calendar, we need to create rows, like [[Monday], [], [11], [25]]
    for i in range(14):

        # Day of the week first
        result = [
            types.InlineKeyboardButton(
                text=f"{day_of_the_week[i%7]}", callback_data="calendar_week"
            ),
        ]

        #               0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15...
        # Here we from [0,0,0,0,1,2,3,4,5,6,7 ,8 ,9 ,10,11,12...]
        # Trying to get ↑             +14                ↑
        for index in range(i, length, 14):
            day = my_calendar[index]

            if day == 0:
                button = types.InlineKeyboardButton(text=" ", callback_data=f"calendar_wrong")
            else:
                text = f"|{day}|" if day == today else f"{day}"
                button = types.InlineKeyboardButton(
                    text=text, callback_data=f"registration_implement_{day}_{month}_{year}"
                )

            result.append(button)

        buttons.append(result)

    buttons.append(
        [
            types.InlineKeyboardButton(
                text=f">>{months_name[next_month]}>>",
                callback_data=f"registration_show_{next_month}_{next_month_year}",
            ),
        ]
    )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    text = "Вибери дату початку минулого циклу:"

    # I am using invisible symbol to center numbers, and it need HTML parsemode
    parse_mode = ParseMode.HTML

    # Change message
    if message_id:
        await executor.bot.edit_message_text(
            text=text,
            chat_id=user_id,
            message_id=message_id,
            reply_markup=keyboard,
            parse_mode=parse_mode,
        )
    # Or send new
    else:
        answer = await executor.bot.send_message(
            text=text, chat_id=user_id, reply_markup=keyboard, parse_mode=parse_mode
        )
        await executor.remember_message(user_id=user_id, message_id=answer.message_id)
