from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = 'админ'
    PROCURATOR = 'прокуратор'
    EDITOR = 'куратор'
    UNKNOWN = 'unknown'
