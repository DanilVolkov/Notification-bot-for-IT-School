from aiogram_dialog import DialogManager

from app.bot.handlers.other_handlers import set_red_question


async def get_recovery_questions(
    dialog_manager: DialogManager, **kwargs
):
    # TODO: получение данных из БД
    list_del_questions = [
        (set_red_question('Что такое хорошо'), 1),
        (set_red_question('Что такое плохо'), 2)
    ]

    return {'list_del_questions': list_del_questions}


async def get_recovery_question(
        dialog_manager: DialogManager, **kwargs
):

    recovery_question = dialog_manager.dialog_data.get('recovery_question')
    recovery_answer = dialog_manager.dialog_data.get('recovery_answer')

    return {
        'recovery_question': recovery_question,
        'recovery_answer': recovery_answer
    }