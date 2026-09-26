from fastapi import FastAPI, HTTPException, status

from schemas.analises import AnaliseSchema
from schemas.caminhos import CaminhoEntradaSchema, CaminhoSchema
from schemas.componentes import ComponentesSchema, IlhaSchema
from schemas.erro import ErroSchema
from schemas.vias import ListaViaSchema
from services.analise import analisar_vias
from services.caminho import caminho_minimo
from services.componentes import encontrar_componentes_conexos, medir_ilha
from services.grafo import montar_grafo

tags_metadata = [
    {"name": "Saúde", "description": "Verifica se a API está no ar"},
    {
        "name": "Componentes",
        "description": "Ilhas de ciclovia (BFS) ordenadas por metros",
    },
    {
        "name": "Caminho mínimo",
        "description": "Menor caminho entre dois nós (Dijkstra), passando por ruas e ciclovias",
    },
    {
        "name": "Análises",
        "description": "Propostas de expansão: ligações entre as ilhas e a malha principal, "
        "ranqueadas por metros conectados / metros a construir",
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
            IlhaSchema(nos=sorted(componente), metros=medir_ilha(grafo, componente))
        )

    ilhas_medidas.sort(key=lambda ilha: ilha.metros, reverse=True)

    resultado = {"total_ilhas": len(componentes), "ilhas": ilhas_medidas}
    return resultado


@app.post(
    "/caminho-minimo",
    response_model=CaminhoSchema,
    tags=["Caminho mínimo"],
    responses={status.HTTP_404_NOT_FOUND: {"model": ErroSchema}},
)
def caminho(dados: CaminhoEntradaSchema):
    """Calcula o menor caminho, em metros, entre dois nós usando Dijkstra.

    Considera ruas e ciclovias. Devolve 404 se não existir caminho entre os nós.
    """
    vias = [via.model_dump() for via in dados.vias]
    grafo = montar_grafo(vias)

    resultado = caminho_minimo(grafo, {dados.origem}, {dados.destino})
    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe caminho entre os nós informados",
        )

    metros, nos = resultado
    return CaminhoSchema(metros=round(metros, 2), nos=nos)


@app.post("/analises", response_model=AnaliseSchema, tags=["Análises"])
def analises(dados: ListaViaSchema):
    """Propõe trechos de rua para virar ciclovia e ligar as ilhas à malha principal.

    A malha principal é a maior ilha em metros. Cada proposta liga uma ilha a ela
    pelo menor caminho (Dijkstra com várias origens). O ranking é feito pela razão
    metros de ciclovia conectados / metros a construir, da maior para a menor.
    """
    vias = [via.model_dump() for via in dados.vias]
    return analisar_vias(vias)
