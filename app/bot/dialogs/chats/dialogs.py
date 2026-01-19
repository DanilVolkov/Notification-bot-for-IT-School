from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Row, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.chats.getters import get_chats, get_copy_chats_name, get_del_chat_name, get_found_chats
from app.bot.dialogs.chats.handlers import save_chat_from_copy, copy_messages, del_chat, confirm_del_chat, find_chat, \
    start_chat_messages_dialog
from app.bot.dialogs.states import ChatsSG
from app.bot.handlers.other_handlers import no_text

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Group(
        SwitchTo(text=Const(buttons_texts.ADD_CHAT), id="btn_add_chat", state=ChatsSG.add_chat),
        SwitchTo(text=Const(buttons_texts.DEL_CHAT), id="btn_del_chat", state=ChatsSG.del_chat),
        width=2,
    ),
    SwitchTo(text=Const(buttons_texts.FIND_CHAT), id="btn_find_chat", state=ChatsSG.find_chat),
    SwitchTo(text=Const(buttons_texts.COPY_MESSAGES), id="btn_copy_messages", state=ChatsSG.copy_messages_from_chat),
    SwitchTo(text=Const(buttons_texts.LIST_CHATS), id="btn_list_chats", state=ChatsSG.list_chats),
    Cancel(Const(buttons_texts.CANCEL), id="btn_chats_cancel"),
    state=ChatsSG.start
)

add_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.ADD_CHATS),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_add_chat_cancel", state=ChatsSG.start),
    state=ChatsSG.add_chat,
)

del_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.DEL_CHAT),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats_for_del",
            item_id_getter=lambda x: x[1],  # TODO: доделать удаление чата по его id
            items="list_chats",
            on_click=confirm_del_chat,
        ),
        id="chats_paginator_for_del",
        width=1,
        height=8,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_del_chat_cancel", state=ChatsSG.start),
    state=ChatsSG.del_chat,
    getter=get_chats,
)

confirm_del_chat_window = Window(
    Format('⚠️ Вы точно хотите удалить чат "{chat_del_id}"?'),  # TODO: изменить на название
    Row(
        Button(text=Const(buttons_texts.YES), id="btn_del_chat_yes", on_click=del_chat),
        SwitchTo(text=Const(buttons_texts.NO), id="btn_del_chat_no", state=ChatsSG.del_chat),
    ),
    state=ChatsSG.del_chat_confirm,
    getter=get_del_chat_name,
)

del_chat_done_window = Window(
    Format('✅ Чат "{chat_del_id}" успешно удален! Можешь меня удалить из списка участников группы.'),  # TODO: изменить на название
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_copy_message_done_chat_cancel", state=ChatsSG.start),
    state=ChatsSG.del_chat_done,
    getter=get_del_chat_name,
)

find_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.FIND_CHAT),
    TextInput(id="chat_input", type_factory=str, on_success=find_chat),
    MessageInput(func=no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_find_chats_cancel", state=ChatsSG.start),
    state=ChatsSG.find_chat,
)

found_chats_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format(text=labels_texts.FOUND_CHATS, when="is_found_chats"),
    Format(text=labels_texts.NOT_FOUND_CHATS, when="is_not_found_chats"),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="found_chats_id",
            item_id_getter=lambda x: x[1],  # TODO: доделать копирование сообщений чата по его id
            items="found_chats",
            on_click=start_chat_messages_dialog,  # TODO: добавить открытие сообщений чата
        ),
        id="found_chats_paginator",
        width=buttons_texts.COUNT_CHATS_WIDTH,
        height=buttons_texts.COUNT_CHATS_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_found_chats_cancel", state=ChatsSG.start),
    state=ChatsSG.found_chats,
    getter=get_found_chats,
)


copy_message_from_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.COPY_CHAT_FROM),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats_for_copy_message_from",
            item_id_getter=lambda x: x[1],  # TODO: доделать копирование сообщений чата по его id
            items="list_chats",
            on_click=save_chat_from_copy,
        ),
        id="chats_paginator_for_copy_message_from",
        width=buttons_texts.COUNT_CHATS_WIDTH,
        height=buttons_texts.COUNT_CHATS_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_copy_message_from_chat_cancel", state=ChatsSG.start),
    state=ChatsSG.copy_messages_from_chat,
    getter=get_chats,
)

copy_message_in_chat_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.COPY_CHAT_IN),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats_for_copy_message_in",
            item_id_getter=lambda x: x[1],  # TODO: доделать копирование сообщений чата по его id
            items="list_chats",
            on_click=copy_messages,
        ),
        id="chats_paginator_for_copy_message_in",
        width=buttons_texts.COUNT_CHATS_WIDTH,
        height=buttons_texts.COUNT_CHATS_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_copy_message_in_chat_cancel", state=ChatsSG.copy_messages_from_chat),
    state=ChatsSG.copy_messages_in_chat,
    getter=get_chats,
)


copy_message_done_window = Window(
    Format('✅ Сообщения успешно скопированы из чата "{chat_from_id}" в чат "{chat_in_id}"'),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_copy_message_done_chat_cancel", state=ChatsSG.start),
    state=ChatsSG.copy_messages_done,
    getter=get_copy_chats_name,
)


list_chats_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    ScrollingGroup(  # TODO: подумать над тем, как сделать лучше визуал
        Select(
            Format("{item[0]}"),
            id="chats",
            item_id_getter=lambda x: x[1],  # TODO: доделать поиск чата по его id для подгрузки данных в него
            items="list_chats",
            on_click=start_chat_messages_dialog
        ),
        id="chats_paginator",
        width=buttons_texts.COUNT_CHATS_WIDTH,
        height=buttons_texts.COUNT_CHATS_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_list_chats_cancel", state=ChatsSG.start),
    state=ChatsSG.list_chats,
    getter=get_chats
)


chats_dialog = Dialog(
    main_window,
    add_chat_window,
    del_chat_window,
    confirm_del_chat_window,
    del_chat_done_window,
    find_chat_window,
    found_chats_window,
    copy_message_from_chat_window,
    copy_message_in_chat_window,
    copy_message_done_window,
    list_chats_window
)
