import pytest

from services.caminho import caminho_minimo


def aresta(grafo, a, b, metros):
    """Adiciona uma aresta não direcionada (nos dois sentidos) ao grafo."""
    grafo.setdefault(a, {})[b] = metros
    grafo.setdefault(b, {})[a] = metros


def triangulo(peso_c_b):
    """Triângulo A=1, B=2, C=3:  1 ─100─ 2,  1 ─10─ 3,  3 ─peso_c_b─ 2."""
    grafo = {}
    aresta(grafo, 1, 2, 100)
    aresta(grafo, 1, 3, 10)
    aresta(grafo, 3, 2, peso_c_b)
    return grafo


def test_prefere_atalho_mais_curto():
    # direto custa 100; pelo C custa 10 + 20 = 30
    metros, caminho = caminho_minimo(triangulo(20), {1}, {2})

    assert metros == pytest.approx(30)
    assert caminho == [1, 3, 2]


def test_mantem_direto_quando_atalho_e_pior():
    # pelo C custaria 10 + 95 = 105, pior que os 100 do direto
    metros, caminho = caminho_minimo(triangulo(95), {1}, {2})

    assert metros == pytest.approx(100)
    assert caminho == [1, 2]


def test_sem_caminho_devolve_none():
    # duas partes soltas: 1-2 e 3-4
    grafo = {}
    aresta(grafo, 1, 2, 10)
    aresta(grafo, 3, 4, 10)

    assert caminho_minimo(grafo, {1}, {4}) is None


def test_origem_igual_destino():
    metros, caminho = caminho_minimo(triangulo(20), {1}, {1})

    assert metros == 0
    assert caminho == [1]


def test_varias_origens_e_destinos():
    # linha 1 ─ 2 ─ 3 ─ 4 ─ 5, cada trecho com 10 m
    # ilha de origem {1, 2}, ilha de destino {4, 5}:
    # deve sair do nó mais próximo (2) e parar no primeiro destino alcançado (4)
    grafo = {}
    for a, b in [(1, 2), (2, 3), (3, 4), (4, 5)]:
        aresta(grafo, a, b, 10)

    metros, caminho = caminho_minimo(grafo, {1, 2}, {4, 5})

    assert metros == pytest.approx(20)
    assert caminho == [2, 3, 4]
