from aiogram_dialog import DialogManager

from app.bot.handlers.other_handlers import set_red_question


async def get_questions(
    dialog_manager: DialogManager, **kwargs
):
    # TODO: получение данных из БД
    list_questions = [
        (set_red_question('Что такое хорошо'), 1),
        (set_red_question('Что такое плохо'), 2)
    ]

    return {'list_questions': list_questions}


async def get_question_info(
        dialog_manager: DialogManager, **kwargs
):

    question = dialog_manager.dialog_data.get('question')
    answer = dialog_manager.dialog_data.get('answer')

    return {
        'question': question,
        'answer': answer
    }
