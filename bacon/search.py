import pickle
from bacon.utils import is_odd, breadth_first_search


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


