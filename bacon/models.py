import pickle

def find(actor_name, target_name="Kevin Bacon", **kwargs):
    database = pickle.load(open('db.p', 'rb'))

    # Check if actor exists
    actor = database['actors'].get(actor_name)
    if not actor:
        pass

    # TODO: If not actor...
    path = breadth_first_search(database, actor_name)

    for index, item in enumerate(path):
        if (index % 2) == 1:
            path[index] = '-({})->'.format(item)
        else:
            path[index] = '{}'.format(item)

    print ' '.join(path)

def breadth_first_search(database, actor, target_actor='Kevin Bacon'):
    queue = list()
    queue.append([actor])

    # Need to alternate between search actors, and searching movies
    count = 0
    while queue:
        # Equivalent to 'dequeue'
        path = queue.pop(0)

        node = path[-1]

        if node == target_actor:
            return path

        if count % 2 == 0:
            relations = database['actors'].get(node, [])
        else:
            relations = database['films'].get(node, [])

        for adjacent in relations:
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

        count += 1