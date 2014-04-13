from StringIO import StringIO
import unittest
from bacon import importer
from bacon.utils import error


class TestImport(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        pass

    def test_bad_directory(self):
        out = StringIO()
        directory = 'bad_folder'
        importer.import_data(directory='bad_folder', out=out)
        output = out.getvalue().strip()

        expected = error('bad folder', directory=directory)
        self.assertEqual(expected, output)

    # No read permissions

    # Test bad folder
    # Test resulting dictionary works
    # Test file read works
    # Test JSON parse works
    # Test skips missing titles


if __name__ == '__main__':
    unittest.main()