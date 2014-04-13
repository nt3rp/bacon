def is_odd(num):
    return num % 2


def default_neighbours_fn(graph, node, level):
    return graph.get(node, [])


def default_valid_path_fn(path):
    return True


def breadth_first_search(graph, start, finish,
        neighbours=default_neighbours_fn, valid_path=default_valid_path_fn
    ):
    queue = list()
    queue.append([start])

    while queue:
        # Equivalent to 'dequeue'
        path = queue.pop(0)

        node = path[-1]

        if node == finish and valid_path(path):
            return path

        adjacent = neighbours(graph, node, len(path)-1)

        for neighbour in adjacent:
            if neighbour not in path:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    return []