from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.message_info import handlers
from app.bot.dialogs.message_info.getters import (
    get_message_datetime,
    get_message_info,
    get_message_name,
    get_message_text,
)
from app.bot.dialogs.states import MessageInfoSG
from app.bot.handlers import other_handlers

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format("{message_info}"),
    SwitchTo(
        Const(buttons_texts.CHANGE_MESSAGE_NAME), id="btn_change_message_name", state=MessageInfoSG.change_message_name
    ),
    SwitchTo(
        Const(buttons_texts.CHANGE_MESSAGE_TEXT), id="btn_change_message_text", state=MessageInfoSG.change_message_text
    ),
    SwitchTo(
        Const(buttons_texts.CHANGE_MESSAGE_DATETIME),
        id="btn_change_message_datetime",
        state=MessageInfoSG.change_message_datetime,
    ),
    SwitchTo(Const(buttons_texts.DEL_MESSAGE), id="btn_del_message", state=MessageInfoSG.del_message_confirm),
    Cancel(Const(buttons_texts.CANCEL), id="btn_message_info_cancel"),
    state=MessageInfoSG.start,
    getter=get_message_info,
)


change_message_name_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format("Текущее название сообщения:\n<code>{message_name}</code>\n\nВведите новое название сообщения"),
    TextInput(id="new_message_name_input", type_factory=str, on_success=handlers.update_message_name),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_message_name_cancel", state=MessageInfoSG.start),
    state=MessageInfoSG.change_message_name,
    getter=get_message_name,
)

change_message_text_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format("Текущий текст сообщения:\n<code>{message_text}</code>\n\n" + f"{labels_texts.TEXT_MESSAGE}"),
    TextInput(id="new_message_text_input", type_factory=str, on_success=handlers.update_message_text),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_message_text_cancel", state=MessageInfoSG.start),
    state=MessageInfoSG.change_message_text,
    getter=get_message_text,
)

change_message_datetime_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format(
        text="Текущие дата и время отправки:\n<code>{message_datetime}</code>\n\n"
        + f"{labels_texts.TIME_SEND_MESSAGE}",
        when="is_datetime",
    ),
    Format(text=f"Текущая дата и время не установлены.\n\n{labels_texts.TIME_SEND_MESSAGE}", when="not_is_datetime"),
    TextInput(
        id="new_message_datetime_input",
        type_factory=other_handlers.datetime_check,
        on_success=handlers.update_message_datetime,
        on_error=other_handlers.error_datetime,
    ),
    MessageInput(func=other_handlers.no_text),
    Row(
        Button(
            Const(buttons_texts.WITHOUT_DATETIME),
            id="btn_without_datetime",
            on_click=handlers.update_message_without_datetime,
        ),
        SwitchTo(Const(buttons_texts.CANCEL), id="btn_change_message_datetime_cancel", state=MessageInfoSG.start),
    ),
    state=MessageInfoSG.change_message_datetime,
    getter=get_message_datetime,
)


confirm_del_message_window = Window(
    Format('⚠️ Вы точно хотите удалить сообщение "{message_name}"?'),  # TODO: изменить на название
    Row(
        Button(text=Const(buttons_texts.YES), id="btn_del_message_yes", on_click=handlers.del_message),
        SwitchTo(text=Const(buttons_texts.NO), id="btn_del_message_no", state=MessageInfoSG.start),
    ),
    state=MessageInfoSG.del_message_confirm,
    getter=get_message_name,
)

del_message_done_window = Window(
    Format('✅ Сообщение "{message_name}" успешно удалено!'),
    # TODO: изменить на название
    SwitchTo(Const(buttons_texts.CANCEL), id="btn_copy_message_done_chat_cancel", state=MessageInfoSG.start),
    state=MessageInfoSG.del_message_done,
    getter=get_message_name,
)


message_info_dialog = Dialog(
    main_window,
    confirm_del_message_window,
    del_message_done_window,
    change_message_name_window,
    change_message_text_window,
    change_message_datetime_window,
)
