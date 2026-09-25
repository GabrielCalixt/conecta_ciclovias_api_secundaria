from geopy.distance import geodesic  # type: ignore


def montar_grafo(vias, tipo=None):
    """exemplo de output:
    {
        1: {2: d12},
        2: {1: d12, 3: d23},
        3: {2: d23, 4: d34},
        4: {3: d34},
    }"""
    grafo = {}
    for via in vias:
        if tipo is not None and tipo != via["tipo"]:
            continue

        # percorrer em pares
        for i in range(len(via["nos"]) - 1):
            origem = via["coordenadas"][i]
            destino = via["coordenadas"][i + 1]
            distancia = geodesic(origem, destino).meters
            grafo.setdefault(via["nos"][i], {}).setdefault(via["nos"][i + 1], distancia)
            grafo.setdefault(via["nos"][i + 1], {}).setdefault(via["nos"][i], distancia)

    return grafo
