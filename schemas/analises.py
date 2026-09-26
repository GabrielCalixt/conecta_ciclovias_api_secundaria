from pydantic import BaseModel

from schemas.componentes import IlhaSchema


class PropostaSchema(BaseModel):
    """Um trecho de rua que, se virar ciclovia, liga uma ilha à malha principal."""

    ilha_nos: list[int]
    metros_ilha: float
    metros_construir: float
    caminho: list[int]
    razao: float


class AnaliseSchema(BaseModel):
    """Resultado da análise: a malha principal e as propostas ranqueadas pela razão."""

    total_ilhas: int
    malha_principal: IlhaSchema | None
    propostas: list[PropostaSchema]
