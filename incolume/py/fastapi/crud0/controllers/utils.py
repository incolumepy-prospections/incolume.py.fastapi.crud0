from enum import Enum, IntFlag, auto


class Role(IntFlag):
    # Sem previlégios pública
    USER = 0
    # leitor
    READER = auto()
    # editor
    EDITOR = auto()
    # Revisor
    PROOFREADER = auto()
    # Gestor/Gerente
    MANAGER = auto()
    # Administrador
    # ADMINISTRATOR = USER | READER | EDITOR | PROOFREADER | MANAGER
    ADMINISTRATOR = auto()


class QueryUser(Enum):
    EMAIL = "email"
    ID = "id"
    NAME = "username"
    USERNAME = "username"
    USER_EMAIL = "email"
    USER_ID = "id"
