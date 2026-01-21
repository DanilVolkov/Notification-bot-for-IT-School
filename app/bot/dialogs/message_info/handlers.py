from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from app.bot.consts import labels_texts
from app.bot.dialogs.states import MessageInfoSG


async def del_message(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    bot = dialog_manager.event.bot
    msg = await bot.send_message(chat_id=callback.from_user.id, text=labels_texts.DEL_MESSAGE_PROCESS)
    # TODO: удаление сообщения из БД
    await msg.delete()
    await dialog_manager.switch_to(state=MessageInfoSG.del_message_done)


async def update_message_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):

    # TODO: изменение имени в БД

    await dialog_manager.switch_to(MessageInfoSG.start)


async def update_message_text(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):

    # TODO: изменение текста в БД

    await dialog_manager.switch_to(MessageInfoSG.start)


async def update_message_datetime(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):

    # TODO: изменение даты в БД

    await dialog_manager.switch_to(MessageInfoSG.start)


async def update_message_without_datetime(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # TODO: изменение даты в БД

    await dialog_manager.switch_to(MessageInfoSG.start)
