import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle


class TestBundlesList(unittest.TestCase, TestBundle):

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
    def test_bundles_list_success(self):
        self.DependenciesFileObject.dependencies_create_file()
        try:
            bundle.bundles_list()
        except Exception as e:
            self.fail(f'bundles_list failed: {e}')
        finally:
            self.DependenciesFileObject.dependencies_remove_file()

    # test errors
    def test_bundles_list_error_dependendencies_file_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            bundle.bundles_list()


if __name__ == '__main__':
    unittest.main()
