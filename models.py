from sqlalchemy import Column, Integer, String, create_engine, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import ClauseElement

db = create_engine('sqlite:///six_degrees.db', echo=True)

Session = sessionmaker(bind=db)
Base = declarative_base()

# Our relations table
film_relations = Table('film_relations', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    actors = relationship('Actor', secondary=film_relations, backref='films')

# TODO: Pass in 'echo' options somehow
# TODO: Check if DB exists before creating
def create_database(*args, **kwargs):
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