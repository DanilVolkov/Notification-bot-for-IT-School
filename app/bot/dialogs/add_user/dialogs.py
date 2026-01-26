from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Row, Select, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.add_user import handlers
from app.bot.dialogs.add_user.getters import get_user_info, get_user_link, get_user_roles
from app.bot.dialogs.states import AddUserSG
from app.bot.handlers.other_handlers import no_text

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.ADD_USER_FIO),
    TextInput(
        id='user_info_input',
        type_factory=handlers.check_user_fio,
        on_success=handlers.save_fio_user,
        on_error=handlers.error_info_user,
    ),
    MessageInput(func=no_text),
    Cancel(Const(buttons_texts.CANCEL)),
    state=AddUserSG.start,
)

add_role_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Const(labels_texts.ADD_USER_ROLE),
    Column(
        Select(
            Format('{item[0]}'),
            id='role_id',
            item_id_getter=lambda x: x[1],
            items='user_roles',
            on_click=handlers.save_user_info,
        ),
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id='btn_add_role_cancel', state=AddUserSG.start),
    state=AddUserSG.add_role,
    getter=get_user_roles,
)

user_info_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Будет сформирована ссылка для пользователя:\n\nℹ️ {user_fio}\n🔑 {user_role}'),
    Row(
        Button(Const(buttons_texts.CREATE_USER_LINK_YES), id='btn_add_link_yes', on_click=handlers.create_user_link),
        Cancel(Const(buttons_texts.CREATE_USER_LINK_NO)),
    ),
    state=AddUserSG.user_info,
    getter=get_user_info,
)


create_link_window = Window(
    Format('🔗 Ссылка для : <a href="{user_link}">нажми на меня</a>'),
    Cancel(Const(buttons_texts.CANCEL), id='btn_create_link_cancel'),
    state=AddUserSG.create_link,
    getter=get_user_link,
)


add_user_dialog = Dialog(main_window, add_role_window, user_info_window, create_link_window)
