def print_matrix(matrix, title):
    print(f'{title}:')
    for row in matrix:
        print(row)
    print()


def adjacency_matrix(vertices, edges_map):
    n = len(vertices)
    # Инициализируем матрицу нулями
    adj = [[0] * n for _ in range(n)]

    # Заполняем матрицу смежности
    for _, (start, end) in edges_map.items():
        adj[start - 1][end - 1] += 1

    return adj


def incidence_matrix(vertices, edges, edges_map):
    n_vertices = len(vertices)
    n_edges = len(edges)
    inc = [[0] * n_edges for _ in range(n_vertices)]

    edge_index = {edge: idx for idx, edge in enumerate(edges)}

    for edge, (start, end) in edges_map.items():
        j = edge_index[edge]
        if start == end:
            inc[start - 1][j] = 2  # Петля
        else:
            inc[start - 1][j] = 1
            inc[end - 1][j] = -1

    return inc


def reachability_matrix(adj_matrix):
    n = len(adj_matrix)

    # Матрица достижимости — начинается как копия матрицы смежности
    reach = [row[:] for row in adj_matrix]

    # Алгоритм: умножаем матрицу до тех пор, пока она не перестанет меняться
    changed = True
    while changed:
        changed = False
        temp = [[0] * n for _ in range(n)]

        # Булево умножение матриц
        for i in range(n):
            for k in range(n):
                if reach[i][k]:
                    for j in range(n):
                        if reach[k][j] and not reach[i][j]:
                            temp[i][j] = 1
                            changed = True

        # Объединение с текущей матрицей достижимости
        for i in range(n):
            for j in range(n):
                if temp[i][j]:
                    reach[i][j] = 1

    # Добавляем диагональ (вершина достижима сама из себя)
    for i in range(n):
        reach[i][i] = 1

    return reach


def strong_components(reach_matrix):
    n = len(reach_matrix)
    visited = [False] * n
    components = []

    for i in range(n):
        if not visited[i]:
            component = []
            for j in range(n):
                if not visited[j] and reach_matrix[i][j] and reach_matrix[j][i]:
                    component.append(j)
                    visited[j] = True
            components.append(component)

    return len(components)


def weak_components(reach_matrix):
    n = len(reach_matrix)
    visited = [False] * n
    components = []

    for i in range(n):
        if not visited[i]:
            component = []
            queue = [i]
            visited[i] = True
            while queue:
                current = queue.pop(0)
                component.append(current)
                for j in range(n):
                    if not visited[j] and (reach_matrix[current][j] or reach_matrix[j][current]):
                        visited[j] = True
                        queue.append(j)
            components.append(component)

    return len(components)


def main():
    # Граф
    vertices = [1, 2, 3, 4, 5]
    edges_map = {
        'I': (5, 1),
        'II': (1, 4),
        'III': (4, 5),
        'IV': (2, 3),
        'V': (4, 4)
    }

    # 1) Матрица смежности
    adj_matrix = adjacency_matrix(vertices, edges_map)
    print_matrix(adj_matrix, 'Матрица смежности')

    # 2) Матрица инцидентности
    inc_matrix = incidence_matrix(vertices, edges_map.keys(), edges_map)
    print_matrix(inc_matrix, 'Матрица инцидентности')

    # 3) Матрица достижимости
    reach_matrix = reachability_matrix(adj_matrix)
    print_matrix(reach_matrix, 'Матрица достижимости')

    # 4) Число связности и число сильной связности
    connectivity = weak_components(reach_matrix)
    strong_connectivity = strong_components(reach_matrix)

    print(f'Число связности: {connectivity}')
    print(f'Число сильной связности: {strong_connectivity}')


if __name__ == '__main__':
    main()
