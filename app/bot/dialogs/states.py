from aiogram.fsm.state import StatesGroup, State

class MenuSG(StatesGroup):
    start = State()


class AccountSG(StatesGroup):
    start = State()


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


class MessagesSG(StatesGroup):
    start = State()
