from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button

from app.bot.dialogs.states import FaqSG


async def set_question_info(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    # TODO: получение из БД ответа на вопрос
    # TODO: получение вопроса по id
    answer = 'Это субъективное понимание поступков, которые совершают люди.'
    question = 'Что такое хорошо и что такое плохо'
    dialog_manager.dialog_data['question_id'] = item_id
    dialog_manager.dialog_data['question'] = question
    dialog_manager.dialog_data['answer'] = answer
    await dialog_manager.switch_to(FaqSG.answer)


async def add_question(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
):
    question = text.strip()
    dialog_manager.dialog_data['new_question'] = question
    await dialog_manager.switch_to(FaqSG.add_answer)


async def add_answer(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
):
    # TODO: запись в БД вопроса и ответа
    dialog_manager.dialog_data['question_id'] = 123456789 # TODO: изменить на id из БД
    dialog_manager.dialog_data['question'] = dialog_manager.dialog_data.get('new_question')
    dialog_manager.dialog_data['answer'] = text.strip()
    await dialog_manager.switch_to(FaqSG.answer)


async def update_question(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
):
    question_id = dialog_manager.dialog_data.get('question_id')
    # TODO: изменение вопроса в БД
    question = 'Что такое хорошо и что такое плохо (обновленный)'
    dialog_manager.dialog_data['question'] = question
    await dialog_manager.switch_to(FaqSG.answer)


async def update_answer(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str,
):
    question_id = dialog_manager.dialog_data.get('question_id')
    # TODO: изменение ответа в БД
    answer = 'Это субъективное понимание поступков, которые совершают люди. (обновленный)'
    dialog_manager.dialog_data['answer'] = answer
    await dialog_manager.switch_to(FaqSG.answer)


async def del_question(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    question_id = dialog_manager.dialog_data.get('question_id')
    # TODO: удаление вопроса из БД
    await dialog_manager.switch_to(FaqSG.del_question_done)