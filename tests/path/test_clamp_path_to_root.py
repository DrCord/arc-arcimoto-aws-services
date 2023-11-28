import tempfile
import unittest
import warnings

from arcimoto_aws_services import path

from tests.dependencies import DependenciesConfigFile
from .path import TestPath


class TestClampPathToRoot(unittest.TestCase, TestPath):

    DependenciesFileObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning,
            message='unclosed.*<ssl.SSLSocket.*>'
        )
        # dependencies.json file must be available for path lib methods to work
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()
        cls.root_dir = path.find_root_directory_path()
        cls.build_dir = tempfile.TemporaryDirectory()
        cls.source = path.clamp_path_to_root(cls.asset_source, cls.root_dir)
        cls.dest = path.clamp_path_to_root(cls.asset_dest, cls.build_dir.name)

    @classmethod
    def tearDownClass(cls):
        cls.build_dir.cleanup()
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_clamp_path_to_root_success(self):
        self.DependenciesFileObject.dependencies_create_file()
        path_clamped_to_root = path.clamp_path_to_root(self.asset_source, self.root_dir)
        self.assertIsInstance(path_clamped_to_root, str)
        self.DependenciesFileObject.dependencies_remove_file()

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
