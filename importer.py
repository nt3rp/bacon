import os
import json
from models import Session, Film, get_or_create, Actor

DIRECTORY = 'films'

def import_data(*args, **kwargs):
    session = Session()

    # Iterate over all files in a folder
    for filename in os.listdir(DIRECTORY):
        contents = None

        full_path = os.path.join(DIRECTORY, filename)

        with open(full_path) as f:
            contents = json.loads(f.read())

        if not contents:
            continue

        title = contents.get('film', {}).get('name')

        if not title:
            continue

        film, _ = get_or_create(session, Film, name=title)
        session.add(film)
        session.commit()

        actors = []
        for cast_member in contents.get('cast'):
            name = cast_member.get('name')

            actor, _ = get_or_create(session, Actor, name=name)
            actors.append(actor)

        session.add_all(actors)
        session.commit()

        film.actors = actors;
        session.add(film)

        session.commit()