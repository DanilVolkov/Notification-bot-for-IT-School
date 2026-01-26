from enum import StrEnum


class UserStatus(StrEnum):
    ADMIN = 'админ'
    PROCURATOR = 'прокуратор'
    EDITOR = 'куратор'
    UNKNOWN = 'unknown'
