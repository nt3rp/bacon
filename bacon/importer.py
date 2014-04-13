import os
import json
import pickle
from bacon import settings


def import_data(directory=None, *args, **kwargs):
    if not directory:
        directory = settings.IMPORT_DIRECTORY

    # Note that our 'database' could probably just be one dictionary.
    # However, since its possible that there are movies and actors
    # that share a name (e.g. "Ed Wood" <- A director, but you get
    # the idea), we break things up into 'actors' and 'films'.
    database = {
        'films': {},
        'actors': {}
    }

    # Iterate over all files in a folder
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)

        with open(full_path) as f:
            try:
                contents = json.loads(f.read())
            except ValueError:
                continue

        title = contents.get('film', {}).get('name')

        if not title:
            continue

        if not database['films'].get(title):
            database['films'][title] = set()


        for actor in contents.get('cast'):
            name = actor.get('name')

            if not database['actors'].get(name):
                database['actors'][name] = set()

            database['actors'][name].add(title)
            database['films'][title].add(name)

    pickle.dump(database, open('db.p', 'wb'))
