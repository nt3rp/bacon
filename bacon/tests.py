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

    # def test_film_title_missing(self):
    #     importer.import_file()

    # Film missing title
    # File contents should match expected

if __name__ == '__main__':
    unittest.main()