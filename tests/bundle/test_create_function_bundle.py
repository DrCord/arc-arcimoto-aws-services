import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle
from tests.TestHelper import TestHelper
from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class TestCreateFunctionBundle(unittest.TestCase, TestBundle):

    function_name = DEFAULT_TEST_LAMBDA_NAME

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )
        cls.DependenciesFileObject = DependenciesConfigFile()

        cls.TestHelperObject = TestHelper()
        cls.TestHelperObject.create_tests_files()

    @classmethod
    def tearDownClass(cls):
        cls.TestHelperObject.remove_tests_folder()
        # remove created dependencies here also file in case of test error
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_create_function_bundle_success(self):
        self.DependenciesFileObject.dependencies_create_file()
        try:
            bundle.create_function_bundle(self.function_name)
        except Exception as e:
            self.fail(f'create_function_bundle failed: {e}')
        finally:
            self.DependenciesFileObject.dependencies_remove_file()

    # test errors
    def test_bundles_list_error_dependendencies_file_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            bundle.create_function_bundle(self.function_name)

    def test_bundles_list_error_input_function_name_no_configuration_found(self):
        self.DependenciesFileObject.dependencies_create_file()
        with self.assertRaises(KeyError):
            bundle.create_function_bundle(f'{self.function_name}-not-really-a-lambda-1234567890')
        self.DependenciesFileObject.dependencies_remove_file()


if __name__ == '__main__':
    unittest.main()
