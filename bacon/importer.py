import os
import json
import pickle
from bacon import Session

DIRECTORY = 'films'

def import_data(*args, **kwargs):
    database = {
        'films': {},
        'actors': {}
    }

    # Iterate over all files in a folder
    for filename in os.listdir(DIRECTORY):
        full_path = os.path.join(DIRECTORY, filename)

        contents = None
        with open(full_path) as f:
            contents = json.loads(f.read())

        if not contents:
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
