from collections import deque


def encontrar_componentes_conexos(grafo):
    """Encontra as ilhas (componentes conexos) do grafo usando BFS.

    Recebe um grafo no formato {no: {vizinho: metros}} e devolve uma lista
    de sets, cada set com os nós de uma ilha. A ordem das ilhas
    não é garantida: ordenar (por exemplo, por metros) é papel de quem chama.

    Complexidade: O(V + E), cada nó e cada aresta são visitados uma vez.
    """
    componentes = []
    visitados = set()

    for raiz in grafo:
        # nó já pertence a uma ilha encontrada antes
        if raiz in visitados:
            continue

        # começa uma nova ilha a partir deste nó
        ilha = {raiz}
        visitados.add(raiz)
        fila = deque([raiz])

        while fila:
            atual = fila.popleft()  # tira da frente
            for vizinho in grafo[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    ilha.add(vizinho)
                    fila.append(vizinho)  # coloca no fim

        componentes.append(ilha)

    return componentes


def medir_ilha(grafo, ilha):
    """Devolve o comprimento total da ilha em metros."""
    soma_total = 0
    for no in ilha:
        soma_do_no = 0
        for aresta in grafo[no]:
            if aresta not in ilha:
                continue
            soma_do_no += grafo[no][aresta]
        soma_total += soma_do_no

    # como toda aresta é somada duas vezes, divida por 2
    return soma_total / 2
