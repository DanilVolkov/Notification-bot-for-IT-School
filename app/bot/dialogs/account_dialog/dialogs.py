from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, SwitchTo, Column, Select, Group, ScrollingGroup
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from app.bot.consts import buttons_texts, labels_texts
from app.bot.consts.buttons_texts import CANCEL
from app.bot.consts.paths import PATH_TO_LOGO
from app.bot.dialogs.account_dialog import handlers
from app.bot.dialogs.account_dialog import getters
from app.bot.dialogs.states import AccountSG
from app.bot.handlers import other_handlers

main_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format(
        '⬇️ Информация о пользователе\n\nℹ️ {find_user_fio}\n🆔 {find_user_id}\n🎭 {find_user_role}\n💫 {find_user_status}',
        when=F['is_admin'],
    ),
    Format('Личный кабинет\n\nℹ️ {find_user_fio}\n🆔 {find_user_id}\n🔑 {find_user_role}', when=~F['is_admin']),
    Group(
        Row(
            Button(
                Const(buttons_texts.ACTIVATE_USER),
                id='btn_status_user_block',
                on_click=handlers.activate_user,
                when=F['is_admin'] & ~F['is_find_user_creator'] & F['is_find_user_blocked'],
            ),
            SwitchTo(
                Const(buttons_texts.BLOCK_USER),
                id='btn_status_user_active',
                when=F['is_admin'] & ~F['is_find_user_creator'] & ~F['is_find_user_blocked'],
                state=AccountSG.block_user
            ),
            SwitchTo(
                Const(buttons_texts.DEL_USER),
                id='btn_del_user',
                when=F['is_admin'] & ~F['is_find_user_creator'],
                state=AccountSG.del_user
            ),
            SwitchTo(
                Const(buttons_texts.CHANGE_USERNAME),
                id='btn_change_username',
                when=F['is_admin'] & ~F['is_find_user_creator'],
                state=AccountSG.change_username
            ),
            SwitchTo(
                Const(buttons_texts.CHANGE_USER_ROLE),
                id='btn_change_user_role',
                when=F['is_admin'] & ~F['is_find_user_creator'],
                state=AccountSG.change_role
            ),
        ),
        width=buttons_texts.COUNT_USER_BUTTON

    ),
    SwitchTo(
        Const(buttons_texts.CHATS_USER),
        id='btn_chats_user',
        when=F['is_admin'] & ~F['is_find_user_creator'],
        state=AccountSG.chats_user
    ),

    Cancel(Const(CANCEL), id='btn_account_cancel'),
    state=AccountSG.start,
    getter=getters.get_account,
)


block_user_window = Window(
    Format('⚠️ Вы точно хотите заблокировать пользователя "{find_user_fio}"?'),
    Row(
        Button(text=Const(buttons_texts.YES), id='btn_block_user_yes', on_click=handlers.block_user),
        SwitchTo(text=Const(buttons_texts.NO), id='btn_block_user_no', state=AccountSG.start),
    ),
    state=AccountSG.block_user,
    getter=getters.get_account,
)

del_user_window = Window(
    Format('⚠️ Вы точно хотите удалить пользователя "{find_user_fio}"?'),
    Row(
        Button(text=Const(buttons_texts.YES), id='btn_block_user_yes', on_click=handlers.del_user),
        SwitchTo(text=Const(buttons_texts.NO), id='btn_block_user_no', state=AccountSG.start),
    ),
    state=AccountSG.del_user,
    getter=getters.get_account,
)


del_user_done_window = Window(
    Format('✅ Пользователь "{del_user_fio}" с id={del_user_id} успешно удален!'),
    Cancel(Const(buttons_texts.CANCEL)),
    state=AccountSG.del_user_done,
    getter=getters.get_del_user_info,
)


change_username_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущее ФИО пользователя:\n<code>{find_user_fio}</code>\n'),
    Const(labels_texts.ADD_USER_FIO),
    TextInput(
        id='user_info_input',
        type_factory=other_handlers.check_user_fio,
        on_success=handlers.save_user_fio,
        on_error=handlers.error_info_user,
    ),
    MessageInput(func=other_handlers.no_text),
    SwitchTo(Const(buttons_texts.CANCEL), id='btn_add_username_cancel', state=AccountSG.start),
    state=AccountSG.change_username,
    getter=getters.get_account,
)


change_user_role_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    Format('Текущая роль пользователя:\n<code>{current_user_role}</code>\n'),
    Const(labels_texts.ADD_USER_ROLE),
    Column(
        Select(
            Format('{item[0]}'),
            id='role_id',
            item_id_getter=lambda x: x[1],
            items='user_roles',
            on_click=handlers.save_user_role,
        ),
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id='btn_add_role_cancel', state=AccountSG.start),
    state=AccountSG.change_role,
    getter=getters.get_user_roles,
)


chats_user_window = Window(
    StaticMedia(path=PATH_TO_LOGO, type=ContentType.PHOTO),
    ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='chats_user',
            item_id_getter=lambda x: x[1],
            items='list_chats',
            on_click=handlers.start_chat_messages_dialog,
        ),
        id='chats_paginator',
        hide_on_single_page=True,
        width=buttons_texts.COUNT_CHATS_WIDTH,
        height=buttons_texts.COUNT_CHATS_HEIGHT,
    ),
    SwitchTo(Const(buttons_texts.CANCEL), id='btn_chats_user_cancel', state=AccountSG.start),
    state=AccountSG.chats_user,
    getter=getters.get_chats,
)


account_dialog = Dialog(
    main_window,
    block_user_window,
    del_user_window,
    del_user_done_window,
    change_username_window,
    change_user_role_window,
    chats_user_window

)
