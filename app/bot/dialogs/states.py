from aiogram.fsm.state import State, StatesGroup


class MenuSG(StatesGroup):
    start = State()


class AccountSG(StatesGroup):
    start = State()
    block_user = State()
    del_user = State()
    del_user_done = State()
    change_username = State()
    change_role = State()
    chats_user = State()


class ChatsSG(StatesGroup):
    start = State()
    add_chat = State()
    del_chat = State()
    del_chat_confirm = State()
    del_chat_done = State()
    find_chat = State()
    found_chats = State()
    copy_messages_from_chat = State()
    copy_messages_in_chat = State()
    copy_messages_done = State()
    list_chats = State()


class ChatMessagesSG(StatesGroup):
    start = State()
    list_messages = State()
    add_message_name = State()
    add_message_text = State()
    add_message_datetime = State()
    change_chat_name = State()
    find_messages = State()
    found_messages = State()
    download_msgs_from_excel = State()
    download_msgs_from_excel_done = State()


class MessageInfoSG(StatesGroup):
    start = State()
    del_message_confirm = State()
    del_message_done = State()
    del_message = State()
    change_message_name = State()
    change_message_text = State()
    change_message_datetime = State()


class UsersSG(StatesGroup):
    start = State()
    list_users = State()


class AddUserSG(StatesGroup):
    start = State()
    add_role = State()
    user_info = State()
    create_link = State()


class RecoverySG(StatesGroup):
    start = State()
    recovery_users = State()
    confirm_recovery_user = State()
    recovery_user_done = State()
    # recovery_chats = State()
    # recovery_messages = State()
    recovery_faqs = State()
