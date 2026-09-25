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
