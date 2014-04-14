import os
import json
import pickle
import sys
from bacon import settings
from bacon.models import FilmGraph


class Importer(object):
    """Handles the importing of film data (actors and film titles)."""
    def __init__(self, out=sys.stdout):
        # Note that our 'database' could probably just be one dictionary.
        # However, since its possible that there are movies and actors
        # that share a name (e.g. "Ed Wood" <- A director, but you get
        # the idea), we break things up into 'actors' and 'films'.
        self._datastore = FilmGraph()
        self.out = out

    @property
    def datastore(self):
        return self._datastore

    @datastore.setter
    def datastore(self, data):
        self._datastore = data

    def load_directory(self, directory):
        """Load film files (assumed to be JSON) from `directory`"""
        self.out.write('Attempting to load files from "{}"... '.format(directory))

        try:
            files = os.listdir(directory)
            self.out.write('Success!\n')
        except:
            # We don't particularly care what the exception is. Just handle it.
            self.out.write(
                'There was a problem accessing "{}"\n'.format(directory)
            )
            return self

        # Iterate over all files in a folder
        for filename in files:
            path = os.path.join(directory, filename)
            self.load_file(path)

        return self

    def load_file(self, path):
        """Load film a film files (assumed to be JSON) from `path`"""
        self.out.write('\tLoading "{}"... '.format(path))
        with open(path) as f:
            self.parse_file(f.read())

        return self

    def parse_file(self, file_contents):
        """Parse contents of film file (assumed to be JSON) into our format."""
        try:
            obj = json.loads(file_contents)
        except ValueError:
            # Skip this file. We only handle JSON right now.
            self.out.write('Skipping (Unsupported format)\n')
            return self

        title = obj.get('film', {}).get('name')

        if not title:
            self.out.write('Skipping (Missing title).\n')
            return self

        for actor in obj.get('cast'):
            name = actor.get('name')
            self._datastore.add_link(name, title)

        self.out.write('Success!\n')
        return self

    def stash(self, filename=None):
        """Pickle our datastore to stash it for later."""
        if not filename:
            filename = settings.STASH_FILENAME

        pickle.dump(self.datastore, open(filename, 'wb'))
        return self

    def from_stash(self, filename=None):
        """Unpickle our datastore for further importing."""
        if not filename:
            filename = settings.STASH_FILENAME

        self.datastore = pickle.load(open(filename, 'rb'))
        return self


def load_directory(
        directory=settings.IMPORT_DIRECTORY,
        store_result=settings.STASH_IMPORTED,
        out=settings.OUTPUT,
        **kwargs
    ):
    importer = Importer(out=out)
    importer.load_directory(directory)
    if store_result:
        importer.stash()

    return importer

def load_file(
        path, store_result=settings.STASH_IMPORTED, out=settings.OUTPUT,*args, **kwargs
    ):
    importer = Importer(out=out)
    importer.load_file(path)
    if store_result:
        importer.stash()

    return importer

def load_stash(filename=None, out=settings.OUTPUT):
    importer = Importer(out=out)
    return importer.from_stash(filename)