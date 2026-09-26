from pydantic import BaseModel, Field

from schemas.vias import ListaViaSchema


class CaminhoEntradaSchema(ListaViaSchema):
    """Vias do bairro + os dois nós entre os quais se quer o menor caminho."""

    origem: int = Field(examples=[1])
    destino: int = Field(examples=[11])


class CaminhoSchema(BaseModel):
    """Menor caminho encontrado pelo Dijkstra."""

    metros: float
    nos: list[int]
