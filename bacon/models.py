import sys
from bacon import settings
from bacon.utils import breadth_first_search, is_odd


class FilmGraph(object):
    """Responsible for handling relationship between actors and films."""

    def __init__(self):
        # Note that our 'datastore' could probably just be one dictionary
        # instead of being separated into two keys (i.e. 'films' and 'actors').
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
        """Create any necessary links between actors and films.

        If the film or actor does not exist yet, it will be created."""
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
        """Find the shortest path from one actor to another.

        :returns:   a list of actors and films. Always of the following form:
                    []
                    [Actor]
                    [Actor, Movie, Actor]
                    ...
        """
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
        """Return the neighbours of node.

        Helper method for breadth first search."""
        key = 'films' if (is_odd(level)) else 'actors'
        return graph.get(key, {}).get(node, [])

    @staticmethod
    def valid_path(path):
        """Determine if path is valid.

        Since we always have a film between two actors,
        a path is valid if it is of odd length."""
        return is_odd(len(path))