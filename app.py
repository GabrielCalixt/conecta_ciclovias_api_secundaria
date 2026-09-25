from fastapi import FastAPI

from schemas.componentes import ComponentesSchema, IlhaSchema
from schemas.vias import ListaViaSchema
from services.componentes import encontrar_componentes_conexos, medir_ilha
from services.grafo import montar_grafo

tags_metadata = [
    {"name": "Saúde", "description": "Verifica se a API está no ar"},
    {
        "name": "Componentes",
        "description": "Ilhas de ciclovia (BFS) ordenadas por metros",
    },
]

app = FastAPI(title="Conecta Ciclovias — API secundária", openapi_tags=tags_metadata)


@app.get("/saude", tags=["Saúde"])
def saude():
    return {"status": "ok"}


@app.post("/componentes", response_model=ComponentesSchema, tags=["Componentes"])
def componentes(dados: ListaViaSchema):
    """Encontra as ilhas de ciclovias e as retorna ordenadas"""
    vias = [via.model_dump() for via in dados.vias]
    grafo = montar_grafo(vias, tipo="ciclovia")
    componentes = encontrar_componentes_conexos(grafo)

    ilhas_medidas: list[IlhaSchema] = []
    for componente in componentes:
        ilhas_medidas.append(
            {"nos": sorted(componente), "metros": medir_ilha(grafo, componente)}
        )

    ilhas_medidas.sort(key=lambda ilha: ilha["metros"], reverse=True)

    resultado = {"total_ilhas": len(componentes), "ilhas": ilhas_medidas}
    return resultado
