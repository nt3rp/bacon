import unittest
from bacon import importer

class ImportTestCase(unittest.TestCase):
    def setUp(self):
        self.db = {
            'films': {},
            'actors': {}
        }

    def tearDown(self):
        pass

    # TODO: provide more meaningful error message
    def test_incorrect_permissions(self):
        try:
            importer.import_directory(directory='tests/wrong_permissions')
        except:
            self.fail('Should not throw an exception for missing folders.')

    # TODO: provide more meaningful error message
    def test_missing_folder(self):
        try:
            importer.import_directory(directory='test/missing_folder')
        except:
            self.fail('Should not throw an exception for missing folders.')

    def test_non_json(self):
        try:
            importer.import_file(full_path='tests/data/non_json.txt', database=self.db)
        except:
            self.fail('Should not throw an exception for non-json file.')

    def test_film_title_missing(self):
        try:
            importer.import_file(full_path='tests/data/missing_title.json', database=self.db)
        except:
            self.fail('Should not throw an exception for missing title.')

    def test_verify_data_single(self):
        importer.import_file(full_path='tests/data/1.json', database=self.db)
        actual = self.db
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

    def test_verify_data_multiple(self):
        importer.import_file(full_path='tests/data/1.json', database=self.db)
        importer.import_file(full_path='tests/data/2.json', database=self.db)

        actual = self.db
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
        importer.import_file(full_path='tests/data/1.json', database=self.db)

        actual = self.db
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

    def test_verify_duplicate_film(self):
        importer.import_file(full_path='tests/data/1.json', database=self.db)
        importer.import_file(full_path='tests/data/1.json', database=self.db)

        actual = self.db
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()