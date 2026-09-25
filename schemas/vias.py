from typing import Literal

from pydantic import BaseModel


# inputs
class ViaSchema(BaseModel):
    id: int
    tipo: Literal["ciclovia", "rua"]
    nos: list[int]
    coordenadas: list[tuple[float, float]]


class ListaViaSchema(BaseModel):
    vias: list[ViaSchema]
