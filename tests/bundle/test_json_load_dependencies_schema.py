import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle


class TestJsonLoadDependenciesSchema(unittest.TestCase, TestBundle):

    DependenciesFileObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_json_load_dependencies_schema_success(self):
        DependenciesFileObject = DependenciesConfigFile()
        DependenciesFileObject.schema_file_create()
        try:
            bundle.json_load_dependencies_schema()
        except Exception as e:
            self.fail(f'json_load_dependencies_schema failed: {e}')
        DependenciesFileObject.schema_file_remove()

    # test errors
    def test_json_load_dependencies_schema_error_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            bundle.json_load_dependencies_schema()

    def test_json_load_dependencies_schema_error_file_contains_invalid_json(self):
        DependenciesFileObject = DependenciesConfigFile()
        DependenciesFileObject.schema_invalid_file_create()
        with self.assertRaises(Exception):
            bundle.json_load_dependencies_schema()
        DependenciesFileObject.schema_invalid_file_remove()


if __name__ == '__main__':
    unittest.main()
