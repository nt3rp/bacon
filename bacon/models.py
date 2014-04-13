from bacon import settings
from bacon.utils import breadth_first_search, is_odd


class FilmGraph(object):
    def __init__(self):
        # Note that our 'database' could probably just be one dictionary.
        # However, since its possible that there are movies and actors
        # that share a name (e.g. "Ed Wood" <- A director, but you get
        # the idea), we break things up into 'actors' and 'films'.

        data = {
            'films': {},
            'actors': {}
        }

        self._datastore = data

    def to_dict(self):
        return self._datastore

    def add_link(self, actor, film):
        if not self._datastore['films'].get(film):
            self._datastore['films'][film] = set()

        if not self._datastore['actors'].get(actor):
            self._datastore['actors'][actor] = set()

        self._datastore['actors'][actor].add(film)
        self._datastore['films'][film].add(actor)

    def find_actor(self, actor):
        return self._datastore['actors'].get(actor)

    def find_film(self, film):
        return self._datastore['films'].get(film)

    def get_shortest_path(self, from_actor, to_actor=None):
        if not to_actor:
            to_actor = settings.TARGET_ACTOR

        path = breadth_first_search(
            self._datastore,
            from_actor,
            to_actor,
            self.neighbours,
            self.valid_path
        )

        return path

    @staticmethod
    def neighbours(graph, node, level):
        key = 'films' if (is_odd(level)) else 'actors'
        return graph.get(key, {}).get(node, [])

    @staticmethod
    def valid_path(path):
        return is_odd(len(path))