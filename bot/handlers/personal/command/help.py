from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from loader import dp

router = Router()
dp.include_router(router)


@router.message(Command("help"))
async def help_command(message: types.Message, state: FSMContext) -> None:
    """
    Command to open command description
    User always can use it
    """
    await state.clear()
    await message.answer(
        text=(
            "В лівому нижньому кутку є кнопка Меню, яка допоможе вам у використанні бота:\n"
            "/start - використовується для того, щоб створити ваш профіль\n"
            "/menu - відкриває головне меню з основними можливостями\n"
            "А саме відкрити меню профілю та емодзі меню\n"
            "/about - відкрити меню інформації про мене\n"
            "Тут ви можете побачити статистику, яку зібрав бот за певну кількість циклів\n"
            "Ви можете відрегагувати цю статистику, якщо вважаєте за потрібне\n"
            "Також ви можете виставити постійні (не статистичні) дані, за якими буде будуватися календар\n"
            "Щоб видалити їх, просто виставте їх значеннями 0\n"
            "/calendar - відкрити календар на актуальному місяці\n"
            "/notification - ще раз відправляє сьогоднішнє повідомлення від бота\n"
            "/reset - ваші дані повністю видаляються, бот перестає відправляти вам повідомлення\n"
            "/help - отримати цей опис\n"
            "/support - написати мені(розробнику)\n"
        ),
    )
