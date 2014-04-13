import os
import json
import pickle
from bacon import settings
from bacon.models import FilmGraph

# TODO: Describe expected format
# TODO: Suppress output during tests

class Importer(object):
    def __init__(self):
        # Note that our 'database' could probably just be one dictionary.
        # However, since its possible that there are movies and actors
        # that share a name (e.g. "Ed Wood" <- A director, but you get
        # the idea), we break things up into 'actors' and 'films'.
        self._datastore = FilmGraph()

    @property
    def datastore(self):
        return self._datastore.to_dict()

    def load_directory(self, directory):
        try:
            files = os.listdir(directory)
        except:  # We don't particularly care what the exception is. Just handle it.
            print('There was a problem accessing "{}"'.format(directory))
            return

        # Iterate over all files in a folder
        for filename in files:
            path = os.path.join(directory, filename)
            load_file(path)

    def load_file(self, path):
        with open(path) as f:
            self.parse_file(f.read())

    def parse_file(self, file_contents):
        try:
            obj = json.loads(file_contents)
        except ValueError:
            # Skip this file. We only handle JSON right now.
            return

        title = obj.get('film', {}).get('name')

        if not title:
            return

        for actor in obj.get('cast'):
            name = actor.get('name')
            self._datastore.add_link(name, title)

    def stash(self):
        # Store the results of our import
        pickle.dump(self.datastore, open(settings.STASH_FILENAME, 'wb'))

    # class method?
    def from_stash(self):
        raise NotImplementedError


def load_directory(
        directory=settings.IMPORT_DIRECTORY,
        store_result=settings.STASH_IMPORTED,
        **kwargs
    ):
    importer = Importer()
    importer.load_directory(directory)
    if store_result:
        importer.stash()

    return importer

def load_file(path, store_result=settings.STASH_IMPORTED, *args, **kwargs):
    importer = Importer()
    importer.load_file(path)
    if store_result:
        importer.stash()

    return importer