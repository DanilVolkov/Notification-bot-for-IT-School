from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CHIEF_EDITOR = "chief editor"
    EDITOR = "editor"
    READER = "reader"
    UNKNOWN = "unknown"
