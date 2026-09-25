from geopy.distance import geodesic

# VIAS_EXEMPLO = [
#     {
#         "id": 10,
#         "tipo": "ciclovia",
#         "nos": [1, 2, 3],
#         "coordenadas": [
#             [-22.9500, -43.1800],
#             [-22.9510, -43.1810],
#             [-22.9520, -43.1820],
#         ],
#     },
#     {
#         "id": 20,
#         "tipo": "rua",
#         "nos": [3, 4],
#         "coordenadas": [[-22.9520, -43.1820], [-22.9530, -43.1830]],
#     },
# ]


""" exemplo de output:
{
    1: {2: d12},
    2: {1: d12, 3: d23},
    3: {2: d23, 4: d34},
    4: {3: d34},
}"""


def montar_grafo(vias, tipo=None):
    """para cada via, preciso: guardar nós, conexões"""
    grafo = {}
    for via in vias:
        if tipo is not None and tipo != via["tipo"]:
            continue

        """armazenar por pares de nós"""
        for i in range(len(via["nos"]) - 1):
            origem = via["coordenadas"][i]
            destino = via["coordenadas"][i + 1]
            distancia = geodesic(origem, destino).meters
            grafo.setdefault(via["nos"][i], {}).setdefault(via["nos"][i + 1], distancia)
            grafo.setdefault(via["nos"][i + 1], {}).setdefault(via["nos"][i], distancia)

    return grafo
