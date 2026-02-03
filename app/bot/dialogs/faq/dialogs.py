from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Row,
    ScrollingGroup,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.faq import getters, handlers
from app.bot.dialogs.states import FaqSG
from app.bot.handlers import other_handlers

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    SwitchTo(
        text=Const(buttons_texts.FAQ_ADD_QUESTION),
        id='btn_add_question',
        state=FaqSG.add_question,
    ),
    SwitchTo(
        text=Const(buttons_texts.FAQ_LIST_QUESTIONS),
        id='btn_list_questions',
        state=FaqSG.list_questions,
    ),
    Cancel(
        text=Const(buttons_texts.CANCEL),
        id='btn_faq_cancel',
    ),
    state=FaqSG.start,
)


add_question_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.QUESTION),
    TextInput(
        id='add_question_text_input',
        type_factory=str,
        on_success=handlers.add_question,
    ),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_add_question_cancel',
        state=FaqSG.start,
    ),
    state=FaqSG.add_question,
    getter=getters.get_question_info,
)


add_answer_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.ANSWER),
    TextInput(
        id='add_answer_text_input',
        type_factory=str,
        on_success=handlers.add_answer,
    ),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_add_answer_cancel',
        state=FaqSG.add_question,
    ),
    state=FaqSG.add_answer,
    getter=getters.get_question_info,
)


list_questions_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.FAQ_QUESTIONS),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format('{item[0]}'),
            id='questions',
            item_id_getter=lambda x: x[1],
            items='list_questions',
            on_click=handlers.set_question_info,
        ),
        id='list_questions_paginator',
        hide_on_single_page=True,
        width=buttons_texts.COUNT_FAQ_WIDTH,
        height=buttons_texts.COUNT_FAQ_HEIGHT,
    ),
    SwitchTo(
        text=Const(buttons_texts.CANCEL),
        id='btn_list_questions_cancel',
        state=FaqSG.start,
    ),
    state=FaqSG.list_questions,
    getter=getters.get_questions,
)


answer_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('❓ {question}?\n\n✅ {answer}'),
    # редактировать вопрос, ответ, удалить вопрос
    Row(
        SwitchTo(
            text=Const(buttons_texts.FAQ_CHANGE_QUESTION),
            id='btn_change_question',
            state=FaqSG.change_question,
        ),
        SwitchTo(
            text=Const(buttons_texts.FAQ_DEL_QUESTION),
            id='btn_del_question',
            state=FaqSG.del_question_confirm,
        ),
    ),
    SwitchTo(
        text=Const(buttons_texts.FAQ_CHANGE_ANSWER),
        id='btn_change_answer',
        state=FaqSG.change_answer,
    ),
    SwitchTo(
        text=Const(buttons_texts.CANCEL),
        id='btn_answer_cancel',
        state=FaqSG.list_questions,
    ),
    state=FaqSG.answer,
    getter=getters.get_question_info,
)


change_question_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущий вопрос: <code>{question}</code>❓\n'),
    Const(labels_texts.QUESTION),
    TextInput(
        id='change_question_text_input',
        type_factory=str,
        on_success=handlers.update_question,
    ),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_change_question_cancel',
        state=FaqSG.answer,
    ),
    state=FaqSG.change_question,
    getter=getters.get_question_info,
)


change_answer_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущий ответ: <code>{answer}</code>\n'),
    Const(labels_texts.ANSWER),
    TextInput(
        id='change_answer_text_input',
        type_factory=str,
        on_success=handlers.update_answer,
    ),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(
        text=Const(buttons_texts.CANCEL),
        id='btn_change_answer_cancel',
        state=FaqSG.answer,
    ),
    state=FaqSG.change_answer,
    getter=getters.get_question_info,
)


confirm_del_question_window = Window(
    Format('⚠️ Вы точно хотите удалить вопрос "{question}"?'),
    Row(
        Button(
            text=Const(buttons_texts.YES),
            id='btn_del_question_yes',
            on_click=handlers.del_question,
        ),
        SwitchTo(
            text=Const(buttons_texts.NO),
            id='btn_del_question_no',
            state=FaqSG.answer,
        ),
    ),
    state=FaqSG.del_question_confirm,
    getter=getters.get_question_info,
)


del_question_done_window = Window(
    Format('✅ Вопрос "{question}" успешно удален!'),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_del_question_done_cancel',
        state=FaqSG.list_questions,
    ),
    state=FaqSG.del_question_done,
    getter=getters.get_question_info,
)


faq_dialog = Dialog(
    main_window,
    add_question_window,
    add_answer_window,
    list_questions_window,
    answer_window,
    change_question_window,
    change_answer_window,
    confirm_del_question_window,
    del_question_done_window,
)
