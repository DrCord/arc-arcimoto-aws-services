import json
import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle
from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class TestLambdaBundleGet(unittest.TestCase, TestBundle):

    function_name = DEFAULT_TEST_LAMBDA_NAME
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
    def test_lambda_bundle_get_success(self):
        self.DependenciesFileObject.dependencies_create_file()
        try:
            bundle.lambda_bundle_get(self.function_name)
        except Exception as e:
            self.fail(f'lambda_bundle_get failed: {e}')
        finally:
            self.DependenciesFileObject.dependencies_remove_file()

    # test errors
    def test_lambda_bundle_get_error_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            bundle.lambda_bundle_get(self.function_name)

    def test_lambda_bundle_get_error_file_contains_invalid_json(self):
        DependenciesFileObject = DependenciesConfigFile()
        DependenciesFileObject.dependencies_invalid_file_create()
        with self.assertRaises(json.decoder.JSONDecodeError):
            bundle.lambda_bundle_get(self.function_name)
        DependenciesFileObject.dependencies_invalid_file_remove()


if __name__ == '__main__':
    unittest.main()
