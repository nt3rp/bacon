def is_odd(num):
    return num % 2


def neighbours(graph, node, level):
    return graph.get(node, [])


def breadth_first_search(graph, start, finish, neighbour_fn=neighbours):
    queue = list()
    queue.append([start])

    while queue:
        # Equivalent to 'dequeue'
        path = queue.pop(0)

        node = path[-1]

        if node == finish:
            return path

        neighbours = neighbour_fn(graph, node, len(path)-1)

        for neighbour in neighbours:
            if neighbour not in path:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    return []