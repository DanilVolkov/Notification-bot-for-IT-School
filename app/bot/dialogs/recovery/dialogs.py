from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.recovery import getters
from app.bot.dialogs.recovery.recovery_chats.windows import (
    confirm_recovery_chat_window,
    list_recovery_chats_window,
    recovery_chat_done_window,
    recovery_messages_for_chat_window,
)
from app.bot.dialogs.recovery.recovery_faq.windows import (
    confirm_recovery_faq_window,
    recovery_faq_done_window,
    recovery_faq_window,
)
from app.bot.dialogs.recovery.recovery_messages.windows import (
    confirm_recovery_message_window,
    list_chats_recovery_messages_window,
    list_del_messages_in_chat_window,
    recovery_messages_done_window,
)
from app.bot.dialogs.recovery.recovery_users.windows import (
    confirm_recovery_user_window,
    recovery_user_done_window,
    recovery_users_window,
)
from app.bot.dialogs.states import RecoverySG

# TODO: на каждое восстановление - своё окно. В сообщениях пишем сокращенно название чата и название сообщения.
# TODO: в сообщение можно зайти и посмотреть о нём доп. инфу
# TODO: сделать также поиск чатов и сообщений
main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.RECOVERY_INFO),
    SwitchTo(
        text=Const(buttons_texts.RECOVERY_CHATS),
        id='btn_recovery_chats',
        when='is_admin',
        state=RecoverySG.recovery_chats,
    ),
    SwitchTo(
        text=Const(buttons_texts.RECOVERY_FAQS),
        id='btn_recovery_faqs',
        when='is_admin',
        state=RecoverySG.recovery_faq,
    ),
    SwitchTo(
        text=Const(buttons_texts.RECOVERY_MESSAGES),
        id='btn_recovery_messages',
        when='is_admin',
        state=RecoverySG.recovery_messages,
    ),
    SwitchTo(
        text=Const(buttons_texts.RECOVERY_USERS),
        id='btn_recovery_users',
        when='is_admin',
        state=RecoverySG.recovery_users,
    ),
    Cancel(Const(buttons_texts.CANCEL)),
    state=RecoverySG.start,
    getter=getters.get_user,
)


# recovery_faqs_window = Window(
#     StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
#     Const(labels_texts.RECOVERY_USERS),
#     ScrollingGroup(
#         Select(
#             Format('{item[0]}'),
#             id='users',
#             item_id_getter=lambda x: x[1],
#             items='list_users',
#             on_click=ru_handlers.get_user_for_recovery,
#         ),
#         id='users_paginator',
#         hide_on_single_page=True,
#         width=buttons_texts.COUNT_USERS_WIDTH,
#         height=buttons_texts.COUNT_USERS_HEIGHT,
#     ),
#     SwitchTo(Const(buttons_texts.CANCEL), id='btn_users_cancel', state=RecoverySG.start),
#     state=RecoverySG.recovery_users,
#     getter=ru_getters.get_users,
# )


recovery_dialog = Dialog(
    main_window,
    recovery_users_window,
    confirm_recovery_user_window,
    recovery_user_done_window,
    list_recovery_chats_window,
    recovery_messages_for_chat_window,
    confirm_recovery_chat_window,
    recovery_chat_done_window,
    list_chats_recovery_messages_window,
    list_del_messages_in_chat_window,
    confirm_recovery_message_window,
    recovery_messages_done_window,
    recovery_faq_window,
    confirm_recovery_faq_window,
    recovery_faq_done_window,
)
