def is_odd(num):
    return num % 2


def default_neighbours_fn(graph, node, level):
    """Default implementation to obtain neighbours from graph.

    For other graphs, we assume that all paths are valid"""
    return graph.get(node, [])


def default_valid_path_fn(path):
    """Default implementation of breadth-first search path validity check.

    For other graphs, we assume that all paths are valid"""
    return True


def breadth_first_search(graph, start, finish,
        neighbours=default_neighbours_fn, valid_path=default_valid_path_fn
    ):
    """A mostly generic breadth-first search implementation.

    This method assumes that nodes in the graph are values rather than objects.
    It would not be too difficult to change this behaviour, but more functions
    would need to be passed in.

    In general, we assume that a graph takes the form of a dictionary of
    adjacency lists:
        {'a': ['b', 'c'], 'c': ['d']}
        # B <- A -> C -> D

    :returns:   a list of nodes from start to finish, or an empty list if no
                path exists between start and finish.
    """
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