import os
import shutil
import tempfile
import unittest
import warnings

from arcimoto_aws_services import (
    bundle,
    path
)

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle


class TestUnzipAsset(unittest.TestCase, TestBundle):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning,
            message='unclosed.*<ssl.SSLSocket.*>'
        )
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()
        cls.root_dir = path.find_root_directory_path()
        cls.build_dir = tempfile.TemporaryDirectory()
        shutil.make_archive('test_archive', 'zip', cls.asset_source)
        cls.source = os.path.join('test_archive.zip')
        cls.dest = path.clamp_path_to_root(cls.asset_dest, cls.build_dir.name)

    @classmethod
    def tearDownClass(cls):
        # remove test_archive.zip file if it exists
        try:
            os.remove('test_archive.zip')
        except Exception:
            pass
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.build_dir.cleanup()

    # test successes
    def test_unzip_asset_success(self):
        try:
            bundle.unzip_asset(self.source, self.dest)
        except Exception as e:
            self.fail(f'unzip_asset failed: {e}')

    # test errors
    def test_unzip_asset_error_source_null(self):
        with self.assertRaises(ValueError):
            bundle.unzip_asset(None, self.dest)

    def test_unzip_asset_error_source_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            bundle.unzip_asset(f'{self.source}-not-folder', self.dest)


if __name__ == '__main__':
    unittest.main()
