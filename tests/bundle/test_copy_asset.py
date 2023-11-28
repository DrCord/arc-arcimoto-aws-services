import tempfile
import unittest
import warnings

from arcimoto_aws_services import (
    bundle,
    path
)

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle


class TestCopyAsset(unittest.TestCase, TestBundle):

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
        cls.source = path.clamp_path_to_root(cls.asset_source, cls.root_dir)
        cls.dest = path.clamp_path_to_root(cls.asset_dest, cls.build_dir.name)

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.build_dir.cleanup()

    # test successes
    def test_copy_asset_success(self):
        try:
            bundle.copy_asset(self.source, self.dest)
        except Exception as e:
            self.fail(f'copy_asset failed: {e}')

    # test errors
    def test_copy_asset_error_source_null(self):
        with self.assertRaises(ValueError):
            bundle.copy_asset(None, self.dest)

    def test_copy_asset_error_source_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            bundle.copy_asset(f'{self.source}-not-folder', self.dest)


if __name__ == '__main__':
    unittest.main()
