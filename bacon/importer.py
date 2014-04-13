import os
import json
import pickle
from bacon import settings


def import_directory(
        directory=settings.IMPORT_DIRECTORY,
        pickling=settings.PICKLING,
        **kwargs
    ):
    # Note that our 'database' could probably just be one dictionary.
    # However, since its possible that there are movies and actors
    # that share a name (e.g. "Ed Wood" <- A director, but you get
    # the idea), we break things up into 'actors' and 'films'.
    database = {
        'films': {},
        'actors': {}
    }

    try:
        files = os.listdir(directory)
    except:  # We don't particularly care what the exception is. Just handle it.
        print('There was a problem accessing "{}"'.format(directory))
        return

    # Iterate over all files in a folder
    for filename in files:
        full_path = os.path.join(directory, filename)
        import_file(database, full_path)

    if pickling:
        pickle.dump(database, open('db.p', 'wb'))

    return database


def import_file(database, full_path, *args, **kwargs):
    with open(full_path) as f:
        contents = parse_file(database, f.read())


def parse_file(database, file):
    try:
        obj = json.loads(file)
    except ValueError:
        return

    title = obj.get('film', {}).get('name')

    if not title:
        return

    if not database['films'].get(title):
        database['films'][title] = set()

    for actor in obj.get('cast'):
        name = actor.get('name')

        if not database['actors'].get(name):
            database['actors'][name] = set()

        database['actors'][name].add(title)
        database['films'][title].add(name)