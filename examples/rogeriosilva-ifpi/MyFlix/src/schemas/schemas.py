from typing import Optional

from pydantic import BaseModel


class Serie(BaseModel):
    id: Optional[int] = None
    titulo: str
    ano: int
    genero: str
    qtd_temporadas: int

    class Config:
        orm_mode = True
