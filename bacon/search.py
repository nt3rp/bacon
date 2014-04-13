import pickle
from bacon.utils import is_odd


def find(actor, target_actor="Kevin Bacon", **kwargs):
    database = pickle.load(open('db.p', 'rb'))

    if not database['actors'].get(actor):
        pass

    path = breadth_first_search(database, actor, target_actor)

    for index, item in enumerate(path):
        if (index % 2) == 1:
            path[index] = '-({})->'.format(item)
        else:
            path[index] = '{}'.format(item)

    print ' '.join(path)


def breadth_first_search(database, actor, target_actor='Kevin Bacon'):
    queue = list()
    queue.append([actor])

    count = 0
    while queue:
        # Equivalent to 'dequeue'
        path = queue.pop(0)

        node = path[-1]

        if node == target_actor:
            return path

        key = 'films' if (is_odd(count)) else 'actors'

        for adjacent in database[key].get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

        count += 1