from aiogram import Router
from aiogram.enums import BotCommandScopeType
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommandScopeChat, Message
from aiogram_dialog import DialogManager, StartMode

from aiogram_dialog_bot import bot
from app.bot.dialogs.states import MenuSG
from app.bot.enums.user_role import UserRole
from app.bot.keyboards.menu_commands import set_main_menu

menu_router = Router()


# @start_session_router.message()
# async def debug_command(message: Message, dialog_manager: DialogManager):
#     print(message.model_dump_json(indent=4, exclude_none=True))


# здесь добавить фильтр на роль пользователя
@menu_router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    # есть ли пользователь в БД, если да - то получение роли
    # если нет - то устанавливаем как для неизвестного
    # если идёт сообщение в чате от пользователя, который есть в списке - реагируем. Иначе нет.
    if message.chat.type == 'private':
        await bot.set_my_commands(
            commands=set_main_menu(UserRole.ADMIN),  # TODO: потом поменять исходя из роли
            scope=BotCommandScopeChat(type=BotCommandScopeType.CHAT, chat_id=message.from_user.id),
        )
        if len(message.text.split()) > 1:
            link = message.text.split()[1]
            # TODO: здесь обращение в redis по ключу

    # await message.answer("Клавиатура удалена.", reply_markup=ReplyKeyboardRemove())

    await dialog_manager.start(state=MenuSG.start, mode=StartMode.RESET_STACK)


@menu_router.message(Command('main_menu'))
async def command_main_menu(message: Message, dialog_manager: DialogManager):
    print('Попал сюда')
    await dialog_manager.start(state=MenuSG.start, mode=StartMode.RESET_STACK)
