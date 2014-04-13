from bacon import settings
from bacon.utils import breadth_first_search, is_odd


class FilmGraph(object):
    def __init__(self):
        # Note that our 'database' could probably just be one dictionary.
        # However, since its possible that there are movies and actors
        # that share a name (e.g. "Ed Wood" <- A director, but you get
        # the idea), we break things up into 'actors' and 'films'.
        self._datastore = {
            'films': {},
            'actors': {}
        }

    def to_dict(self):
        return self._datastore

    def add_link(self, actor, film):
        if not self._datastore['films'].get(film):
            self._datastore['films'][film] = set()

        if not self._datastore['actors'].get(actor):
            self._datastore['actors'][actor] = set()

        self._datastore['actors'][actor].add(film)
        self._datastore['films'][film].add(actor)

    def get_shortest_path(self, from_actor, to_actor=None):
        if not to_actor:
            to_actor = settings.TARGET_ACTOR

        path = breadth_first_search(
            self._datastore,
            from_actor,
            to_actor,
            self.neighbours
        )

        return path

    @staticmethod
    def neighbours(graph, node, level):
        key = 'films' if (is_odd(level)) else 'actors'
        return graph.to_dict()[key].get(node, [])