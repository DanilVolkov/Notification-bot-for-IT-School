from aiogram.types import BotCommand

from app.bot.consts.commands import COMMANDS_UNKNOWN, COMMANDS_USER
from app.bot.enums.user_role import UserRole


def set_main_menu(role):
    if role == UserRole.UNKNOWN:
        return [BotCommand(command='/start', description=COMMANDS_UNKNOWN['/start'])]
    else:
        return [
            BotCommand(command='/start', description=COMMANDS_USER['/start']),
            BotCommand(command='/help', description=COMMANDS_USER['/help']),
            BotCommand(command='/main_menu', description=COMMANDS_USER['/main_menu']),
        ]
