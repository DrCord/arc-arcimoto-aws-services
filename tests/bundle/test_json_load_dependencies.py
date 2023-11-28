import json
import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle


class TestJsonLoadDependencies(unittest.TestCase, TestBundle):

    DependenciesFileObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )
        cls.DependenciesFileObject = DependenciesConfigFile()

    @classmethod
    def tearDownClass(cls):
        # remove created dependencies here also file in case of test error
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_json_load_dependencies_success(self):
        self.DependenciesFileObject.dependencies_create_file()
        try:
            bundle.json_load_dependencies()
        except Exception as e:
            self.fail(f'json_load_dependencies failed: {e}')
        finally:
            self.DependenciesFileObject.dependencies_remove_file()

    # test errors
    def test_json_load_dependencies_error_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            bundle.json_load_dependencies()

    def test_json_load_dependencies_error_file_contains_invalid_json(self):
        DependenciesFileObject = DependenciesConfigFile()
        DependenciesFileObject.dependencies_invalid_file_create()
        with self.assertRaises(json.decoder.JSONDecodeError):
            bundle.json_load_dependencies()
        DependenciesFileObject.dependencies_invalid_file_remove()


if __name__ == '__main__':
    unittest.main()
