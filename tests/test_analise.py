import pytest
from test_componentes import VIAS_EXEMPLO

from services.analise import analisar_vias

# Ilha isolada: ciclovia sem nenhuma via (nem rua) ligando ao resto do mapa
ILHA_ISOLADA = {
    "id": 104,
    "tipo": "ciclovia",
    "nos": [20, 21],
    "coordenadas": [[-22.9700, -43.2000], [-22.9710, -43.2010]],
}


def test_analise_exemplo_gera_uma_proposta():
    resultado = analisar_vias(VIAS_EXEMPLO)

    assert resultado["total_ilhas"] == 2
    assert resultado["malha_principal"]["nos"] == [1, 2, 3, 5]
    assert len(resultado["propostas"]) == 1

    proposta = resultado["propostas"][0]
    assert proposta["ilha_nos"] == [10, 11]
    # sai da malha principal pelo nó 5, passa pela rua (4) e chega na ilha (10)
    assert proposta["caminho"] == [5, 4, 10]
    assert proposta["metros_construir"] > 0
    assert proposta["razao"] == pytest.approx(
        proposta["metros_ilha"] / proposta["metros_construir"], abs=0.01
    )


def test_analise_ignora_ilha_sem_caminho():
    resultado = analisar_vias(VIAS_EXEMPLO + [ILHA_ISOLADA])

    assert resultado["total_ilhas"] == 3
    ilhas_propostas = [p["ilha_nos"] for p in resultado["propostas"]]
    assert [20, 21] not in ilhas_propostas
    assert ilhas_propostas == [[10, 11]]


def test_analise_sem_ciclovias():
    so_ruas = [via for via in VIAS_EXEMPLO if via["tipo"] == "rua"]

    resultado = analisar_vias(so_ruas)

    assert resultado == {"total_ilhas": 0, "malha_principal": None, "propostas": []}


def test_analise_propostas_ordenadas_por_razao():
    # segunda ilha extra ligada à malha principal por uma rua longa
    extra = [
        {
            "id": 105,
            "tipo": "ciclovia",
            "nos": [30, 31],
            "coordenadas": [[-22.9400, -43.1700], [-22.9401, -43.1701]],
        },
        {
            "id": 202,
            "tipo": "rua",
            "nos": [1, 30],
            "coordenadas": [[-22.9500, -43.1800], [-22.9400, -43.1700]],
        },
    ]

    resultado = analisar_vias(VIAS_EXEMPLO + extra)

    razoes = [p["razao"] for p in resultado["propostas"]]
    assert len(razoes) == 2
    assert razoes == sorted(razoes, reverse=True)
