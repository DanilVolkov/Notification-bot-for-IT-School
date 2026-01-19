from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from app.bot.consts import labels_texts


async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.answer(labels_texts.NO_TEXT)