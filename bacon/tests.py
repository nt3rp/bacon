import unittest
from bacon import importer


class ImportTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Folder or file problems should not raise an exception
    def test_missing_folder(self):
        try:
            importer.import_directory(directory='bogus_folder')
        except:
            self.fail('Should not throw an exception for missing folders.')

    # Film missing title
    # File contents should match expected

if __name__ == '__main__':
    unittest.main()