from enum import Enum


class MessageStatus(str, Enum):
    SENT = "Отправлено"
    PLANNED = "Запланировано"
    DRAFT = "Черновик"
