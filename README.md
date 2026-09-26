# Conecta Ciclovias — API secundária

Serviço de **regra de negócio** do projeto *Conecta Ciclovias*, um planejador de expansão de ciclovias para o Rio de Janeiro.

A malha de ciclovias de um bairro costuma ser formada por **ilhas desconectadas**: trechos soltos que não se ligam uns aos outros. Esta API recebe as vias de um bairro (ciclovias e ruas) e responde três perguntas:

1. **Quais são as ilhas de ciclovia**, e qual o tamanho de cada uma em metros?
2. **Qual é o menor caminho** entre dois pontos da malha viária?
3. **Onde construir** para ligar cada ilha à malha principal com o **menor número de metros construídos**?

Ela é uma **calculadora sem estado**: não acessa a internet nem banco de dados. Quem busca os dados no OpenStreetMap (Overpass API) e guarda os resultados é a [API principal](https://github.com/GabrielCalixt/conecta_ciclovias_api_principal), que chama esta API via REST.

---

## Algoritmos (implementados à mão, sem bibliotecas de grafos)

| Etapa | Algoritmo | Complexidade | Onde fica |
|---|---|---|---|
| Montar o grafo a partir das vias | Lista de adjacência com pesos em metros (distância geodésica) | O(nós das vias) | `services/grafo.py` |
| Encontrar as ilhas de ciclovia | **BFS** (busca em largura) para achar os componentes conexos | O(V + E) | `services/componentes.py` |
| Medir cada ilha | Soma das arestas internas (cada aresta contada uma vez) | O(V + E) | `services/componentes.py` |
| Menor caminho | **Dijkstra com várias origens**, usando fila de prioridade (`heapq`) | O((V + E) log V) | `services/caminho.py` |
| Propostas de expansão | BFS + Dijkstra, ranqueados por `metros da ilha / metros a construir` | — | `services/analise.py` |

---

## Rotas

Documentação interativa (Swagger) em **http://localhost:8000/docs**.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/saude` | Healthcheck. Devolve `{"status": "ok"}` |
| POST | `/componentes` | Vias → ilhas de ciclovia, ordenadas por metros |
| POST | `/caminho-minimo` | Vias + `origem` + `destino` → menor caminho em metros. Devolve **404** se não existir caminho |
| POST | `/analises` | Vias → malha principal + propostas de ligação ranqueadas |

### Formato de entrada (comum às rotas POST)

```json
{
  "vias": [
    {"id": 101, "tipo": "ciclovia", "nos": [1, 2, 3],
     "coordenadas": [[-22.95, -43.18], [-22.951, -43.181], [-22.952, -43.182]]},
    {"id": 201, "tipo": "rua", "nos": [3, 4],
     "coordenadas": [[-22.952, -43.182], [-22.953, -43.183]]}
  ]
}
```

- `tipo` aceita só `"ciclovia"` ou `"rua"`. Qualquer outro valor devolve **422**.
- `nos[i]` fica na posição `coordenadas[i]`, no formato `[latitude, longitude]`.
- Duas vias que compartilham o mesmo ID de nó estão conectadas nesse ponto (um cruzamento).

### Exemplo de resposta de `/analises`

```json
{
  "total_ilhas": 2,
  "malha_principal": {"nos": [1, 2, 3, 5], "metros": 452.82},
  "propostas": [
    {"ilha_nos": [10, 11], "metros_ilha": 150.94, "metros_construir": 301.9,
     "caminho": [5, 4, 10], "razao": 0.5}
  ]
}
```

A **razão** indica quantos metros de ciclovia passam a ficar conectados para cada metro construído. Quanto maior, melhor o investimento.

---

## Instalação e execução local

Pré-requisito: Python 3.14.

```bash
git clone https://github.com/GabrielCalixt/conecta_ciclovias_api_secundaria.git
cd conecta_ciclovias_api_secundaria

python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Acesse **http://localhost:8000/docs**.

### Testes e lint

```bash
pytest          # testes unitários (algoritmos) e de integração (rotas)
ruff check .    # lint
ruff format .   # formatação
```

No Windows, o script `verificar.ps1` roda tudo em sequência e para no primeiro erro:

```powershell
.\verificar.ps1
```

---

## Execução com Docker

Pré-requisito: [Docker](https://docs.docker.com/get-docker/) instalado e em execução.

```bash
docker build -t conecta-ciclovias-secundaria .
docker run --rm -p 8000:8000 conecta-ciclovias-secundaria
```

Acesse **http://localhost:8000/docs**.

Para subir esta API junto com a principal, use o `docker-compose.yml` que fica no repositório da **API principal**. As instruções estão no README de lá.

---

## Estrutura de pastas

```
app.py              # rotas FastAPI
schemas/            # formatos de entrada e saída (Pydantic)
services/           # algoritmos: grafo, BFS, Dijkstra, análise
tests/              # testes unitários e de integração (pytest)
Dockerfile
requirements.txt
```

---

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/): API REST e Swagger automático
- [Pydantic](https://docs.pydantic.dev/): validação de entrada e saída
- [geopy](https://geopy.readthedocs.io/): distância geodésica entre coordenadas
- [pytest](https://docs.pytest.org/) e [ruff](https://docs.astral.sh/ruff/): testes e lint

Projeto desenvolvido para o MVP da disciplina de Arquitetura de Software, na pós-graduação em Engenharia de Software da PUC-Rio.
