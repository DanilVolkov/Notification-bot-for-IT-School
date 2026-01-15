from aiogram import Router
from aiogram.enums import BotCommandScopeType
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommandScopeChat, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from aiogram_dialog_bot import bot
from app.bot.dialogs.states import MenuSG
from app.bot.enums.roles import UserRole
from app.bot.keyboards.menu_commands import set_main_menu

start_session_router = Router()

# здесь добавить фильтр на роль пользователя
@start_session_router.message(CommandStart())
async def command_start_process(message: Message,
                                dialog_manager: DialogManager):
    # есть ли пользователь в БД, если да - то получение роли
    # если нет - то устанавливаем как для неизвестного
    # если идёт сообщение в чате от пользователя, который есть в списке - реагируем. Иначе нет.
    if message.chat.type == "private":
        await bot.set_my_commands(
            commands=set_main_menu(UserRole.ADMIN),  # TODO: потом поменять исходя из роли
            scope=BotCommandScopeChat(
                type=BotCommandScopeType.CHAT,
                chat_id=message.from_user.id
            )
        )

    #await message.answer("Клавиатура удалена.", reply_markup=ReplyKeyboardRemove())

    await dialog_manager.start(
        state=MenuSG.main_menu,
        mode=StartMode.RESET_STACK
    )
