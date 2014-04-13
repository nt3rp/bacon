from bacon import settings
from bacon.importer import load_stash


def find(actor, target_actor=settings.TARGET_ACTOR, datastore=None, **kwargs):
    if not datastore:
        importer = load_stash()
        datastore = importer.datastore

    path = datastore.get_shortest_path(actor, target_actor)

    for index, item in enumerate(path):
        if (index % 2) == 1:
            path[index] = '-({})->'.format(item)
        else:
            path[index] = '{}'.format(item)

    print ' '.join(path)


