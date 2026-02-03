from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Row,
    ScrollingGroup,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.recovery.recovery_faq import getters, handlers
from app.bot.dialogs.states import RecoverySG

recovery_faq_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.RECOVERY_QUESTION),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format('{item[0]}'),
            id='questions',
            item_id_getter=lambda x: x[1],
            items='list_del_questions',
            on_click=handlers.set_recovery_question_info,
        ),
        id='list_del_questions_paginator',
        hide_on_single_page=True,
        width=buttons_texts.COUNT_FAQ_WIDTH,
        height=buttons_texts.COUNT_FAQ_HEIGHT,
    ),
    SwitchTo(
        text=Const(buttons_texts.CANCEL),
        id='btn_del_questions_cancel',
        state=RecoverySG.start,
    ),
    state=RecoverySG.recovery_faq,
    getter=getters.get_recovery_questions,
)

confirm_recovery_faq_window = Window(
    Format(
        '❓ {recovery_question}?\n\n✅ {recovery_answer}\n\n'
        '⚠️ Вы точно хотите восстановить вопрос?'
    ),
    Row(
        Button(
            text=Const(buttons_texts.YES),
            id='btn_recovery_faq_yes',
            on_click=handlers.recovery_question,
        ),
        SwitchTo(
            text=Const(buttons_texts.NO),
            id='btn_recovery_faq_no',
            state=RecoverySG.recovery_faq,
        ),
    ),
    state=RecoverySG.confirm_recovery_faq,
    getter=getters.get_recovery_question,
)

recovery_faq_done_window = Window(
    Format('✅ Вопрос "{recovery_question}" успешно восстановлен!'),
    SwitchTo(
        Const(buttons_texts.CANCEL),
        id='btn_recovery_faq_cancel',
        state=RecoverySG.recovery_faq,
    ),
    state=RecoverySG.recovery_faq_done,
    getter=getters.get_recovery_question,
)
