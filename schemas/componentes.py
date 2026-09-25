from pydantic import BaseModel


class IlhaSchema(BaseModel):
    nos: list[int]
    metros: float


class ComponentesSchema(BaseModel):
    total_ilhas: int
    ilhas: list[IlhaSchema]
