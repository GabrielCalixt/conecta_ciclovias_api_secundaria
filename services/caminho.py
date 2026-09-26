import heapq


def caminho_minimo(grafo, origens: set, destinos: set):
    """Menor caminho (em metros) de QUALQUER nó de `origens` até QUALQUER nó de `destinos`.

    Dijkstra com várias origens: todas as origens começam na fila com distância 0,
    e a busca para no primeiro destino que sai da fila (a distância dele é
    definitiva, porque os pesos nunca são negativos).

    Devolve (metros, caminho) ou None se não existir caminho.
    Complexidade: O((V + E) log V), por causa da fila de prioridade (heapq).
    """
    distancia = {}  # melhor distância conhecida até cada nó
    anterior = {}  # de onde viemos, para reconstruir o caminho
    fila = []  # heap de tuplas (distância, nó): sempre sai o MENOR

    # 1. todas as origens entram com distância 0
    for origem in origens:
        distancia[origem] = 0
        heapq.heappush(fila, (0, origem))

    while fila:
        # 2. tira o nó mais próximo
        dist_atual, atual = heapq.heappop(fila)

        # 3. cópia velha na fila (já achamos caminho melhor para este nó): pula
        if dist_atual > distancia[atual]:
            continue

        # 4. chegou a um destino: reconstrói o caminho de trás para frente
        if atual in destinos:
            caminho = [atual]
            while caminho[-1] in anterior:
                caminho.append(anterior[caminho[-1]])
            return dist_atual, caminho[::-1]

        # 5. tenta melhorar a distância de cada vizinho
        for vizinho, metros in grafo.get(atual, {}).items():
            nova_dist = dist_atual + metros
            if nova_dist < distancia.get(vizinho, float("inf")):
                distancia[vizinho] = nova_dist
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))

    # 6. fila acabou sem alcançar nenhum destino
    return None
