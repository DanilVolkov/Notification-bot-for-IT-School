from aiogram.fsm.state import StatesGroup, State

class MenuSG(StatesGroup):
    main_menu = State()


class AccountSG(StatesGroup):
    start = State()