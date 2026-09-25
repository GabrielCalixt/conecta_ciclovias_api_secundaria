import pytest

from services.componentes import encontrar_componentes_conexos, medir_ilha
from services.grafo import montar_grafo

# Mapa do exemplo:
#
#   ciclovia 101:  1 ── 2 ── 3            ┐ ilha A = {1, 2, 3, 5}
#   ciclovia 102:            3 ── 5       ┘ (duas vias unidas pelo nó 3)
#   rua      201:                 5 ── 4 ── 10
#   ciclovia 103:                           10 ── 11   ilha B = {10, 11}
#
# Só com ciclovias: 2 ilhas. Com a rua: tudo vira 1 componente.
VIAS_EXEMPLO = [
    {
        "id": 101,
        "tipo": "ciclovia",
        "nos": [1, 2, 3],
        "coordenadas": [
            [-22.9500, -43.1800],
            [-22.9510, -43.1810],
            [-22.9520, -43.1820],
        ],
    },
    {
        "id": 102,
        "tipo": "ciclovia",
        "nos": [3, 5],
        "coordenadas": [[-22.9520, -43.1820], [-22.9530, -43.1830]],
    },
    {
        "id": 103,
        "tipo": "ciclovia",
        "nos": [10, 11],
        "coordenadas": [[-22.9550, -43.1850], [-22.9560, -43.1860]],
    },
    {
        "id": 201,
        "tipo": "rua",
        "nos": [5, 4, 10],
        "coordenadas": [
            [-22.9530, -43.1830],
            [-22.9540, -43.1840],
            [-22.9550, -43.1850],
        ],
    },
]


def como_conjunto(componentes):
    """Converte a lista de ilhas num conjunto de frozensets, para comparar sem depender da ordem."""
    return {frozenset(componente) for componente in componentes}


def verificar_invariantes(componentes, grafo):
    """Regras que valem para QUALQUER resultado de encontrar_componentes_conexos."""
    nos = set(grafo)
    todos = set().union(*componentes) if componentes else set()
    # ninguém fica de fora
    assert todos == nos, f"nós esperados {nos}, encontrados {todos}"
    # ninguém aparece em duas ilhas
    assert sum(len(c) for c in componentes) == len(nos), "algum nó aparece repetido"


# ---------- encontrar_componentes_conexos (BFS) ----------


def test_componentes_grafo_vazio():
    assert encontrar_componentes_conexos({}) == []


def test_componentes_apenas_ciclovias():
    grafo = montar_grafo(VIAS_EXEMPLO, tipo="ciclovia")

    componentes = encontrar_componentes_conexos(grafo)

    # a ilha A é formada por DUAS vias (101 e 102) unidas pelo nó 3
    assert como_conjunto(componentes) == {frozenset({1, 2, 3, 5}), frozenset({10, 11})}
    verificar_invariantes(componentes, grafo)


def test_componentes_grafo_completo():
    # teste do ALGORITMO: a rua 201 liga as duas ilhas, então a BFS
    # precisa atravessar vias diferentes e devolver um componente só
    grafo = montar_grafo(VIAS_EXEMPLO)

    componentes = encontrar_componentes_conexos(grafo)

    assert como_conjunto(componentes) == {frozenset(grafo)}
    verificar_invariantes(componentes, grafo)


# ---------- medir_ilha ----------

# grafo feito à mão, com pesos redondos: 1 ──100── 2 ──50── 3
GRAFO_MANUAL = {1: {2: 100}, 2: {1: 100, 3: 50}, 3: {2: 50}}


def test_medir_ilha_conta_cada_aresta_uma_vez():
    # somar a lista de adjacência inteira daria 300 (cada aresta aparece 2x)
    assert medir_ilha(GRAFO_MANUAL, {1, 2, 3}) == pytest.approx(150)


def test_medir_ilha_ignora_arestas_para_fora_da_ilha():
    # a aresta 2-3 sai da ilha {1, 2}, então não entra na conta
    assert medir_ilha(GRAFO_MANUAL, {1, 2}) == pytest.approx(100)


def test_medir_ilha_de_um_no_so():
    assert medir_ilha(GRAFO_MANUAL, {1}) == 0


GRAFO_TRIANGULO = {1: {2: 10, 3: 30}, 2: {1: 10, 3: 20}, 3: {1: 30, 2: 20}}


def test_medir_ilha_com_ciclo():
    assert medir_ilha(GRAFO_TRIANGULO, {1, 2, 3}) == pytest.approx(60)
