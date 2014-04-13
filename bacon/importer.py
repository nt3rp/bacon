import os
import json
from bacon import Session
from bacon.models import Film, get_or_create, Actor

DIRECTORY = 'films'

def import_data(*args, **kwargs):
    session = Session()

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

        film = Film(name=title)

        actors = []
        for cast_member in contents.get('cast'):
            name = cast_member.get('name')

            actor = Actor(name=name)
            actors.append(actor)

        session.add_all(actors)

        film.actors = actors;
        session.add(film)

    session.commit()