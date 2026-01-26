from enum import StrEnum


class MessageStatus(StrEnum):
    SENT = 'отправлено'
    PLANNED = 'запланировано'
    DRAFT = 'черновик'
