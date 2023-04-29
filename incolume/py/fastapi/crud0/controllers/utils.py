from enum import Enum, Flag, auto


class Role(Flag):
    USER = 0  # Sem previlégios apenas
    READER = auto()  # leitor
    EDITOR = auto()  # editor
    PROOFREADER = auto()  # Revisor
    ADMINISTRATOR = USER | READER | EDITOR | PROOFREADER  # Administrador


class QueryUser(Enum):
    EMAIL = 'email'
    ID = 'id'
    NAME = 'username'
    USERNAME = 'username'
    USER_EMAIL = 'email'
    USER_ID = 'id'
