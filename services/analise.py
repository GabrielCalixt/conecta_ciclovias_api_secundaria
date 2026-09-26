from services.caminho import caminho_minimo
from services.componentes import encontrar_componentes_conexos, medir_ilha
from services.grafo import montar_grafo


def analisar_vias(vias):
    """Propõe onde construir ciclovia para ligar as ilhas à malha principal.

    1. Monta o grafo só de ciclovias e encontra as ilhas (BFS).
    2. A maior ilha, em metros, é a malha principal.
    3. Para cada outra ilha, o Dijkstra com várias origens encontra o menor trecho,
       no grafo completo (ruas + ciclovias), entre a malha principal e a ilha.
    4. Ranqueia pela razão = metros de ciclovia conectados / metros a construir.
       Quanto maior a razão, mais ciclovia se ganha por metro construído.

    Ilhas sem nenhum caminho até a malha principal ficam fora do ranking.

    Simplificação conhecida: `metros_construir` é o comprimento total do caminho,
    mesmo que algum trecho dele já seja ciclovia de outra ilha.
    """
    grafo_ciclovias = montar_grafo(vias, tipo="ciclovia")
    grafo_completo = montar_grafo(vias)
    ilhas = encontrar_componentes_conexos(grafo_ciclovias)

    if not ilhas:
        return {"total_ilhas": 0, "malha_principal": None, "propostas": []}

    ilhas_medidas = [(medir_ilha(grafo_ciclovias, ilha), ilha) for ilha in ilhas]
    ilhas_medidas.sort(key=lambda item: item[0], reverse=True)
    metros_principal, malha_principal = ilhas_medidas[0]

    propostas = []
    for metros_ilha, ilha in ilhas_medidas[1:]:
        resultado = caminho_minimo(grafo_completo, malha_principal, ilha)
        if resultado is None:
            continue
        metros_construir, caminho = resultado
        # evita divisão por zero se os pontos coincidirem (dado ruidoso do OSM)
        razao = metros_ilha / max(metros_construir, 1.0)
        propostas.append(
            {
                "ilha_nos": sorted(ilha),
                "metros_ilha": metros_ilha,
                "metros_construir": round(metros_construir, 2),
                "caminho": caminho,
                "razao": round(razao, 2),
            }
        )

    propostas.sort(key=lambda proposta: proposta["razao"], reverse=True)

    return {
        "total_ilhas": len(ilhas),
        "malha_principal": {"nos": sorted(malha_principal), "metros": metros_principal},
        "propostas": propostas,
    }
