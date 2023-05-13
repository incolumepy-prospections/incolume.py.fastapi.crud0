"""Module utils."""

from enum import Enum, IntEnum, IntFlag, auto


class Role(IntFlag):
    """Schema for Role."""

    # Sem previlégios - status de criação default (somente acesso público)
    USER = 0
    # leitor - poderá ler versões anteriores dos itens
    READER = auto()
    # editor - poderá ler/editar versões anteriores dos itens
    EDITOR = auto()
    # Revisor - poderá ler/atualizar items
    PROOFREADER = auto()
    # Gestor/Gerente - poderá gerenciar/conceder privilégios
    # dos perfis e todas as permissões anteriores
    MANAGER = auto()
    # Administrador - poderá gerenciar/conceder privilégios
    # dos perfis e todas as permissões anteriores
    # ADMINISTRATOR = USER | READER | EDITOR | PROOFREADER | MANAGER
    ADMINISTRATOR = auto()


class Roles(str, Enum):
    """Schema for Roles."""

    # Sem previlégios - status de criação default (somente acesso público)
    USER = "USER"
    # leitor - poderá ler versões anteriores dos itens
    READER = "READER"
    # editor - poderá ler/editar versões anteriores dos itens
    EDITOR = "EDITOR"
    # Revisor - poderá ler/atualizar items
    PROOFREADER = "PROOFREADER"
    # Gestor/Gerente - poderá gerenciar/conceder privilégios
    # dos perfis e todas as permissões anteriores
    MANAGER = "MANAGER"
    # Administrador - poderá gerenciar/conceder privilégios
    # dos perfis e todas as permissões anteriores
    ADMINISTRATOR = "ADMINISTRATOR"


class QueryUser(Enum):
    """Schema for QueryUser."""

    EMAIL = "email"
    ID = "id"
    NAME = "username"
    USERNAME = "username"
    USER_EMAIL = "email"
    USER_ID = "id"


class ToggleBool(Enum):
    """Schema for ToggleBool."""

    ON = True
    OFF = False


class Sort(Enum):
    """Schema for Sort."""

    ASCENDING = 0
    DESCENDING = 1

    def __call__(self, values):
        """Call this class."""
        return sorted(values, reverse=self is Sort.DESCENDING)
