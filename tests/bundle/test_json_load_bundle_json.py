import json
import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle
from tests.bundles import TestBundles
from tests.TestHelper import TestHelper
from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class TestJsonLoadBundleJson(unittest.TestCase, TestBundle):

    function_name = DEFAULT_TEST_LAMBDA_NAME
    lambda_bundle_name = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.TestHelperObject = TestHelper()
        cls.TestBundlesObject = TestBundles()

        cls.DependenciesFileObject.dependencies_create_file()
        cls.lambda_bundle_name = bundle.lambda_bundle_get(cls.function_name)

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_json_load_bundle_json_success(self):
        self.TestHelperObject.create_tests_files()
        try:
            bundle.json_load_bundle_json(self.lambda_bundle_name)
        except Exception as e:
            self.fail(f'json_load_bundle_json failed: {e}')
        finally:
            self.TestHelperObject.remove_tests_folder()

    # test errors
    def test_json_load_bundle_json_error_bundle_name_file_path_not_found(self):
        self.TestHelperObject.create_tests_files()
        with self.assertRaises(FileNotFoundError):
            bundle.json_load_bundle_json(f'{self.lambda_bundle_name}-not-really-a-lambda-bundle-1234567890')
        self.TestHelperObject.remove_tests_folder()

    def test_json_load_bundle_json_error_file_contains_invalid_json(self):
        self.TestBundlesObject.bundle_json_invalid_file_create()
        with self.assertRaises(json.decoder.JSONDecodeError):
            bundle.json_load_bundle_json(self.lambda_bundle_name)
        self.TestBundlesObject.bundle_json_invalid_file_remove()


if __name__ == '__main__':
    unittest.main()
