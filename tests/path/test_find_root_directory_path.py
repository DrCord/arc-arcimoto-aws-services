import unittest
import warnings

from arcimoto_aws_services import path

from tests.dependencies import DependenciesConfigFile


class TestFindRootDirectoryPath(unittest.TestCase):
    ''' test path.find_root_directory_path '''

    DependenciesFileObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning,
            message='unclosed.*<ssl.SSLSocket.*>'
        )
        cls.DependenciesFileObject = DependenciesConfigFile()

    @classmethod
    def tearDownClass(cls):
        # remove created dependencies here also file in case of test error
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_find_root_directory_path_success(self):
        self.DependenciesFileObject.dependencies_create_file()
        root_directory_path = path.find_root_directory_path()
        self.assertIsInstance(root_directory_path, str)
        self.DependenciesFileObject.dependencies_remove_file()

    # test errors
    # None to test


if __name__ == '__main__':
    unittest.main()
