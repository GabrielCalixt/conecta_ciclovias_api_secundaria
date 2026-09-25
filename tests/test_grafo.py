import copy

from services.grafo import montar_grafo

# Entrada no formato do CONTRATO: uma lista de vias (e não um grafo pronto).
# Quem transforma as vias em grafo é a função montar_grafo, e é isso que o teste verifica.
# Via 10 (ciclovia) passa pelos nós 1 -> 2 -> 3. Via 20 (rua) liga 3 -> 4.
# O nó 3 é compartilhado: é ele que conecta as duas vias.
VIAS_EXEMPLO = [
    {
        "id": 10,
        "tipo": "ciclovia",
        "nos": [1, 2, 3],
        "coordenadas": [
            [-22.9500, -43.1800],
            [-22.9510, -43.1810],
            [-22.9520, -43.1820],
        ],
    },
    {
        "id": 20,
        "tipo": "rua",
        "nos": [3, 4],
        "coordenadas": [[-22.9520, -43.1820], [-22.9530, -43.1830]],
    },
]


def verificar_invariantes(grafo):
    """Regras que valem para QUALQUER grafo gerado por montar_grafo."""
    for no, vizinhos in grafo.items():
        assert no not in vizinhos, f"nó {no} é vizinho de si mesmo"
        for vizinho, distancia in vizinhos.items():
            assert distancia > 0, f"aresta {no}-{vizinho} com distância {distancia}"
            assert vizinho in grafo, f"vizinho {vizinho} não existe como nó do grafo"
            assert grafo[vizinho].get(no) == distancia, (
                f"aresta {no}-{vizinho} não é simétrica"
            )


# testa a montagem do grafo com todas as vias (ciclovias e ruas)
def test_montar_grafo_completo():
    grafo = montar_grafo(VIAS_EXEMPLO)

    assert set(grafo) == {1, 2, 3, 4}
    assert set(grafo[1]) == {2}
    assert set(grafo[2]) == {1, 3}
    assert set(grafo[3]) == {2, 4}
    assert set(grafo[4]) == {3}
    assert 3 not in grafo[1], "nós 1 e 3 não são vizinhos diretos"
    verificar_invariantes(grafo)


# testa o filtro: só ciclovias entram (o nó 4 só existia na rua)
def test_montar_grafo_filtrando_ciclovias():
    grafo = montar_grafo(VIAS_EXEMPLO, tipo="ciclovia")

    assert set(grafo) == {1, 2, 3}
    assert 4 not in grafo
    assert set(grafo[3]) == {2}
    verificar_invariantes(grafo)


# a função lê as vias, mas nunca as altera
def test_montar_grafo_nao_altera_entrada():
    copia = copy.deepcopy(VIAS_EXEMPLO)

    montar_grafo(VIAS_EXEMPLO)

    assert VIAS_EXEMPLO == copia


# caso de borda: sem vias, grafo vazio (e sem erro)
def test_montar_grafo_sem_vias():
    assert montar_grafo([]) == {}
