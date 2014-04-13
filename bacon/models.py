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

    def add_link(self, actor, film):
        if not self._datastore['films'].get(film):
            self._datastore['films'][film] = set()

        if not self._datastore['actors'].get(actor):
            self._datastore['actors'][actor] = set()

        self._datastore['actors'][actor].add(film)
        self._datastore['films'][film].add(actor)

    def to_dict(self):
        return self._datastore