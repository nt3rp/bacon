import os
import json
from bacon import settings

# TODO: Describe expected format
# TODO: Suppress output during tests

class Importer(object):
    def __init__(self):
        # Note that our 'database' could probably just be one dictionary.
        # However, since its possible that there are movies and actors
        # that share a name (e.g. "Ed Wood" <- A director, but you get
        # the idea), we break things up into 'actors' and 'films'.
        self.datastore = {
            'films': {},
            'actors': {}
        }

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

        if not self.datastore['films'].get(title):
            self.datastore['films'][title] = set()

        for actor in obj.get('cast'):
            name = actor.get('name')

            if not self.datastore['actors'].get(name):
                self.datastore['actors'][name] = set()

            self.datastore['actors'][name].add(title)
            self.datastore['films'][title].add(name)


def load_directory(directory=settings.IMPORT_DIRECTORY, **kwargs):
    importer = Importer()
    importer.load_directory(directory)
    return importer

def load_file(path, *args, **kwargs):
    importer = Importer()
    importer.load_file(path)
    return importer