from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.bot.dialogs.states import MainMenuSG

start_session_router = Router()


@start_session_router.message(CommandStart())
async def command_start_process(message: Message,
                                dialog_manager: DialogManager):
    await dialog_manager.start(
        state=MainMenuSG.main_menu,
        mode=StartMode.RESET_STACK
    )
