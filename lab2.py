# Исходное множество
M = {2, 3, 4, 5, 8, 9, 12, 25}
sorted_M = sorted(M)
size = len(sorted_M)

# 1. Построение исходного отношения R
R = [(a, b) for a in M for b in M if a * a == b]


# 2. Матрица отношения
def relation_to_matrix(relation):
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for a, b in relation:
        i = sorted_M.index(a)
        j = sorted_M.index(b)
        matrix[i][j] = 1
    return matrix


matrix_R = relation_to_matrix(R)

# 3. Противоположное отношение R'
opposite_R = [(a, b) for a in M for b in M if (a, b) not in R]
matrix_opposite_R = relation_to_matrix(opposite_R)

# 4. Обратное отношение R^{-1}
inverse_R = [(b, a) for (a, b) in R]
matrix_inverse_R = relation_to_matrix(inverse_R)


# 5. Составное отношение R∘R
composite_R = set()
for a, b1 in R:
    for b2, c in R:
        if b1 == b2:
            composite_R.add((a, c))
composite_R = list(composite_R)
matrix_composite_R = relation_to_matrix(composite_R)


# 6. Транзитивное замыкание R+
def transitive_closure(matrix):
    n = len(matrix)
    reach = matrix.copy()
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return reach


matrix_transitive_R = transitive_closure(matrix_R)

# 7. Рефлексивное замыкание R∪
reflexive_R = set(R)
for x in M:
    reflexive_R.add((x, x))
matrix_reflexive_R = relation_to_matrix(reflexive_R)


# Функции для проверки свойств
def is_reflexive(rel, m_set):
    return all((x, x) in rel for x in m_set)


def is_symmetric(rel):
    return all((b, a) in rel for (a, b) in rel)


def is_antisymmetric(rel):
    return all(a == b for (a, b) in rel if (b, a) in rel)


def is_transitive(rel):
    return all((a, c) in rel for (a, b1) in rel for (b2, c) in rel if b1 == b2)


# Проверка свойств для всех отношений
relations = {
    'R': R,
    'R''': opposite_R,
    'R^-1': inverse_R,
    'R∘R': composite_R,
    'R+': list(zip(sorted_M, sorted_M)),  # Для транзитивного замыкания используем матрицу
    'R∪': reflexive_R
}

print('\nПроверка свойств отношений:')
for name, rel in relations.items():
    print(f'\nОтношение {name}:')
    r_set = set(rel)
    print('  Рефлексивность:', is_reflexive(r_set, M))
    print('  Симметричность:', is_symmetric(r_set))
    print('  Антисимметричность:', is_antisymmetric(r_set))
    print('  Транзитивность:', is_transitive(r_set))


# Вывод матриц
def print_matrix(name, matrix):
    print(f'\nМатрица {name}:')
    for row in matrix:
        print(f'  {row}')


print_matrix('R', matrix_R)
print_matrix('R''', matrix_opposite_R)
print_matrix('R^-1', matrix_inverse_R)
print_matrix('R∘R', matrix_composite_R)
print_matrix('R+', matrix_transitive_R)
print_matrix('R∪', matrix_reflexive_R)
