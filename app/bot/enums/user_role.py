from enum import StrEnum


class UserRole(StrEnum):
    CREATOR = 'создатель'
    ADMIN = 'админ'
    PROCURATOR = 'прокуратор'
    EDITOR = 'куратор'
    UNKNOWN = 'неопознан'
