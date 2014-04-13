import unittest
from bacon import importer

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

        actual = instance.datastore
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

    def test_verify_data_multiple(self):
        instance = importer.load_file('tests/data/1.json')
        instance.load_file('tests/data/2.json')

        actual = instance.datastore
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

        actual = instance.datastore
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

    def test_verify_duplicate_film(self):
        instance = importer.load_file('tests/data/1.json')
        instance.load_file('tests/data/1.json')

        actual = instance.datastore
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)


class SearchTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()