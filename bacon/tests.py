import json
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

    # Folder or file problems should not raise an exception
    # TODO: How can we test things like permissions?
    def test_missing_folder(self):
        try:
            importer.import_directory(directory='bogus_folder')
        except:
            self.fail('Should not throw an exception for missing folders.')

    def test_non_json(self):
        try:
            importer.parse_file(self.db, 'This is not json')
        except:
            self.fail('Should not throw an exception for non-json file.')

    def test_film_title_missing(self):
        try:
            importer.parse_file(self.db, json.dumps({'film': {}}))
        except:
            self.fail('Should not throw an exception for missing title.')

    def test_verify_data_single(self):
        importer.parse_file(self.db, json.dumps({
            'film': {'name': 'Film 1'},
            'cast': [{'name': 'Actor 1'}]
        }))
        actual = self.db
        expected = {
            'films': {'Film 1': set(['Actor 1'])},
            'actors': {'Actor 1': set(['Film 1'])}
        }
        self.assertDictEqual(expected, actual)

    def test_verify_data_multiple(self):
        importer.parse_file(self.db, json.dumps({
            'film': {'name': 'Film 1'},
            'cast': [{'name': 'Actor 1'}]
        }))
        importer.parse_file(self.db, json.dumps({
            'film': {'name': 'Film 2'},
            'cast': [{'name': 'Actor 1'}, {'name': 'Actor 2'}]
        }))

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

    # test duplicate actor
    # test duplicate film

if __name__ == '__main__':
    unittest.main()