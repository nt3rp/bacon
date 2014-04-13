import unittest
from bacon import importer
from bacon.models import FilmGraph


class ImportTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # TODO: provide more meaningful error message
    def test_incorrect_permissions(self):
        try:
            importer.load_directory(directory='tests/wrong_permissions')
        except:
            self.fail('Should not throw an exception for missing folders.')

    # TODO: provide more meaningful error message
    def test_missing_folder(self):
        try:
            importer.load_directory('test/missing_folder')
        except:
            self.fail('Should not throw an exception for missing folders.')

    def test_non_json(self):
        try:
            importer.load_file('tests/data/non_json.txt')
        except:
            self.fail('Should not throw an exception for non-json file.')

    def test_film_title_missing(self):
        try:
            importer.load_file('tests/data/missing_title.json')
        except:
            self.fail('Should not throw an exception for missing title.')

    def test_verify_data_single(self):
        instance = importer.load_file('tests/data/1.json')

        actual = instance.datastore.to_dict()
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

    def test_verify_data_multiple(self):
        instance = importer.load_file('tests/data/1.json')
        instance.load_file('tests/data/2.json')

        actual = instance.datastore.to_dict()
        expected = {
            'films': {
                'Film 1': set(['Actor 1']),
                'Film 2': set(['Actor 1', 'Actor 2'])
            },
            'actors': {
                'Actor 1': set(['Film 1', 'Film 2']),
                'Actor 2': set(['Film 2'])
            }
        }
        self.assertDictEqual(expected, actual)

    def test_verify_duplicate_actor(self):
        instance = importer.load_file('tests/data/1.json')

        actual = instance.datastore.to_dict()
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

    def test_verify_duplicate_film(self):
        instance = importer.load_file('tests/data/1.json')
        instance.load_file('tests/data/1.json')

        actual = instance.datastore.to_dict()
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)


class FilmGraphTestCase(unittest.TestCase):
    def setUp(self):
        self.datastore = FilmGraph()

    def tearDown(self):
        pass

    def test_empty_datastore(self):
        expected = []
        actual = self.datastore.get_shortest_path('Anyone')
        self.assertListEqual(expected, actual)

    def test_no_such_actor(self):
        self.datastore.add_link('John Crichton', 'Farscape')

        expected = []
        actual = self.datastore.get_shortest_path('Aeryn Sun')
        self.assertListEqual(expected, actual)

    def test_no_such_target_actor(self):
        self.datastore.add_link('John Crichton', 'Farscape')

        expected = []
        actual = self.datastore.get_shortest_path(
            'John Crichton', 'Future Crichton'
        )
        self.assertListEqual(expected, actual)

    def test_no_films_in_common(self):
        self.datastore.add_link('Superman', 'The Adventures of Lois and Clark')
        self.datastore.add_link('Clark Kent', 'Superman')

        expected = []
        actual = self.datastore.get_shortest_path('Clark Kent', 'Superman')
        self.assertListEqual(expected, actual)

    def test_start_is_finish(self):
        self.datastore.add_link('Somebody to Love', 'Queen')

        expected = ['Somebody to Love']
        actual = self.datastore.get_shortest_path(
            'Somebody to Love', 'Somebody to Love'
        )
        self.assertListEqual(expected, actual)

    def test_start_is_finish(self):
        self.datastore.add_link('Bill Murray', 'Ghostbusters')
        self.datastore.add_link('Bill Murray', 'SNL')
        self.datastore.add_link('John Belushi', 'SNL')
        self.datastore.add_link('John Belushi', 'Blues Brothers')
        self.datastore.add_link('Dan Aykroyd', 'Ghostbusters')
        self.datastore.add_link('Dan Aykroyd', 'Blues Brothers')

        expected = ['Bill Murray', 'Ghostbusters', 'Dan Aykroyd']
        actual = self.datastore.get_shortest_path('Bill Murray', 'Dan Aykroyd')
        self.assertListEqual(expected, actual)


class StashTestCase(unittest.TestCase):
    def setUp(self):
        self.datastore = FilmGraph()

    def tearDown(self):
        pass

    def test_stash_and_load(self):
        instance = importer.load_file('tests/data/1.json')
        instance.load_file('tests/data/2.json')

        expected = instance.datastore.to_dict()

        instance.stash('test.p')
        instance.from_stash('test.p')

        actual = instance.datastore.to_dict()
        self.assertDictEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()