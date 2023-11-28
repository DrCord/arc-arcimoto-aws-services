import json
import os
import tempfile
import unittest
import warnings


from arcimoto_aws_services import path

from .path import TestPath


class TestCreateArchive(unittest.TestCase, TestPath):

    file_name = 'test_create_archive.json'

    @classmethod
    def setUpClass(cls):
        cls.build_dir = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.build_dir.cleanup()

    # test successes
    def test_create_archive_success(self):
        # without ignore warnings generates ResourceWarning: unclosed file <_io.BufferedRandom name=4>
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            json_object = json.dumps({}, indent=4)
            with open(os.path.join(self.build_dir.name, self.file_name), 'w') as outfile:
                outfile.write(json_object)
            self.assertIsInstance(path.create_archive(self.build_dir.name), str)

    # test errors
    def test_create_archive_error_source_null(self):
        # without ignore warnings generates ResourceWarning: unclosed file <_io.BufferedRandom name=4>
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with self.assertRaises(TypeError):
                path.create_archive(None)


if __name__ == '__main__':
    unittest.main()
