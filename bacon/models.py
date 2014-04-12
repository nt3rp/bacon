from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import ClauseElement

# Our relations table
from bacon import Base, Session

film_relations = Table('film_relations', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Actor(name='{}')>".format(self.name)

    # Basically, just an alias to make our breadth-first search more generic
    def relations(self):
        return self.films


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    actors = relationship('Actor', secondary=film_relations, backref='films')

    def __repr__(self):
        return "<Film(name='{}')>".format(self.name)

    # Basically, just an alias to make our breadth-first search more generic
    def relations(self):
        return self.actors

# TODO: Pass in 'echo' options somehow
# TODO: Check if DB exists before creating
def create_database(db, *args, **kwargs):
    Base.metadata.create_all(db)

# http://stackoverflow.com/a/2587041/165988
def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True

def find(actor_name, target_name="Kevin Bacon", **kwargs):
    session = Session()

    # Basically, do a breadth-first search

    # Find actor
    actor = session.query(Actor).filter(Actor.name == actor_name).first()

    # TODO: If not actor...
    path = breadth_first_search(actor)

    for index, item in enumerate(path):
        if (index % 2) == 1:
            path[index] = '-({})->'.format(item.name)
        else:
            path[index] = '{}'.format(item.name)

    print ' '.join(path)

def breadth_first_search(actor, target_name='Kevin Bacon'):
    queue = []
    queue.append([actor])

    while queue:
        # Equivalent to 'dequeue'
        path = queue.pop(0)

        node = path[-1]

        if node.name == target_name:
            return path

        for adjacent in node.relations():
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)