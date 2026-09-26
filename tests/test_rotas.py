from fastapi import status
from fastapi.testclient import TestClient
from test_componentes import VIAS_EXEMPLO

from app import app

client = TestClient(app)


def test_saude():

    response = client.get("/saude")
    assert response.status_code == status.HTTP_200_OK, (
        f"serviço com status {response.status_code}"
    )

    assert response.json() == {"status": "ok"}


def test_componentes_happy_path():

    response = client.post("/componentes", json={"vias": VIAS_EXEMPLO})

    assert response.status_code == status.HTTP_200_OK, (
        f"serviço com status {response.status_code}"
    )

    resultado = response.json()

    assert resultado["total_ilhas"] == 2, f"total de ilhas: {resultado['total_ilhas']}"
    assert resultado["ilhas"][0]["nos"] == [1, 2, 3, 5]
    assert resultado["ilhas"][0]["metros"] >= resultado["ilhas"][1]["metros"]


VIA_INVALIDA = [
    {
        "id": 101,
        "tipo": "estrada",
        "nos": [1, 2, 3],
        "coordenadas": [
            [-22.9500, -43.1800],
            [-22.9510, -43.1810],
            [-22.9520, -43.1820],
        ],
    }
]


def test_input_invalido():

    resultado = client.post("/componentes", json={"vias": VIA_INVALIDA})
    assert resultado.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_caminho_minimo_happy_path():
    corpo = {"vias": VIAS_EXEMPLO, "origem": 1, "destino": 11}

    response = client.post("/caminho-minimo", json=corpo)

    assert response.status_code == status.HTTP_200_OK
    resultado = response.json()
    # sai da ilha A, passa pela rua (5 -> 4 -> 10) e chega na ilha B
    assert resultado["nos"] == [1, 2, 3, 5, 4, 10, 11]
    assert resultado["metros"] > 0


def test_caminho_minimo_sem_caminho_404():
    vias_soltas = [
        {
            "id": 1,
            "tipo": "rua",
            "nos": [1, 2],
            "coordenadas": [[-22.95, -43.18], [-22.951, -43.181]],
        },
        {
            "id": 2,
            "tipo": "rua",
            "nos": [3, 4],
            "coordenadas": [[-22.96, -43.19], [-22.961, -43.191]],
        },
    ]

    response = client.post(
        "/caminho-minimo", json={"vias": vias_soltas, "origem": 1, "destino": 4}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_analises_happy_path():
    response = client.post("/analises", json={"vias": VIAS_EXEMPLO})

    assert response.status_code == status.HTTP_200_OK
    resultado = response.json()
    assert resultado["total_ilhas"] == 2
    assert resultado["malha_principal"]["nos"] == [1, 2, 3, 5]
    assert resultado["propostas"][0]["caminho"] == [5, 4, 10]
