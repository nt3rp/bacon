from bacon import settings
from bacon.importer import load_stash


def find(
    actor, target_actor=settings.TARGET_ACTOR, datastore=None, out=settings.OUTPUT, **kwargs
    ):
    if not datastore:
        importer = load_stash()
        datastore = importer.datastore

    out.write('Finding the link between "{}" and "{}"...\n\n'.format(
        actor, target_actor
    ))
    path = datastore.get_shortest_path(actor, target_actor)

    for index, item in enumerate(path):
        if (index % 2) == 1:
            path[index] = '-({})->'.format(item)
        else:
            path[index] = '{}'.format(item)

    if not len(path):
        out.write('Sorry, we found no link between "{}" and "{}" :(\n'.format(
            actor, target_actor
        ))
    else:
        out.write('\t' + ' '.join(path) + '\n')


