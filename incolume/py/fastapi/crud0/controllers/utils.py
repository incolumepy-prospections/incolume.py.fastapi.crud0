from enum import Enum, Flag, auto


class Role(Flag):
    USER = 0  # Sem previlégios apenas
    READER = auto()  # leitor
    EDITOR = auto()  # editor
    PROOFREADER = auto()  # Revisor
    ADMINISTRATOR = USER | READER | EDITOR | PROOFREADER  # Administrador


class QueryUser(Enum):
    ID = 0
    USERNAME = 1
    EMAIL = 2
    USER_ID = 0
    NAME = 1
    USER_EMAIL = 2
