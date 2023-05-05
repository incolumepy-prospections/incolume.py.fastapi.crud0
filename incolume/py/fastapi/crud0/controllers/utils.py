from enum import Enum, IntEnum, IntFlag, auto


class Role(IntFlag):
    # Sem previlégios - status de criação default (somente acesso público)
    USER = 0
    # leitor - poderá ler versões anteriores dos itens
    READER = auto()
    # editor - poderá ler/editar versões anteriores dos itens
    EDITOR = auto()
    # Revisor - poderá ler/atualizar items
    PROOFREADER = auto()
    # Gestor/Gerente - poderá gerenciar/conceder privilégios dos perfis e todas as permissões anteriores 
    MANAGER = auto()
    # Administrador - poderá gerenciar/conceder privilégios dos perfis e todas as permissões anteriores 
    # ADMINISTRATOR = USER | READER | EDITOR | PROOFREADER | MANAGER
    ADMINISTRATOR = auto()


class QueryUser(Enum):
    EMAIL = "email"
    ID = "id"
    NAME = "username"
    USERNAME = "username"
    USER_EMAIL = "email"
    USER_ID = "id"
