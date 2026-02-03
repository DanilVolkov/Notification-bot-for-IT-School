from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from app.bot.dialogs.states import RecoverySG


async def set_recovery_question_info(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    # TODO: получение из БД ответа на вопрос
    # TODO: получение вопроса по id
    recovery_answer = 'Это субъективное понимание поступков, которые совершают люди.'
    recovery_question = 'Что такое хорошо и что такое плохо'
    dialog_manager.dialog_data['recovery_question_id'] = item_id
    dialog_manager.dialog_data['recovery_question'] = recovery_question
    dialog_manager.dialog_data['recovery_answer'] = recovery_answer
    await dialog_manager.switch_to(RecoverySG.confirm_recovery_faq)


async def recovery_question(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    recovery_question_id = dialog_manager.dialog_data.get('recovery_question_id')
    # TODO: восстановление вопроса - перенос пользователя из таблицы удалённых
    await dialog_manager.switch_to(state=RecoverySG.recovery_faq_done)