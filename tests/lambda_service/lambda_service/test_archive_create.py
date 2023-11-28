import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestArchiveCreate(unittest.TestCase):

    parser = None
    LambdaServiceObject = None
    TestHelperObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

        cls.TestHelperObject = TestHelper()
        cls.function_name = cls.TestHelperObject.function_name

        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file(cls.function_name)

        cls.TestHelperObject.create_tests_files(cls.function_name)

        cls.LambdaServiceObject = LambdaService(verbose=False)

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestHelperObject.remove_tests_folder()

    # test successes
    def test_archive_create_success(self):
        try:
            self.LambdaServiceObject.archive_create(
                function_name=self.function_name,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    def test_archive_create_error_input_function_name_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.archive_create(
                function_name=1234567890,
                mute=True
            )

    def test_archive_create_error_input_mute_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.archive_create(
                function_name=self.function_name,
                mute='not-a-Boolean'
            )

    def test_archive_create_error_input_function_name_no_configuration_found(self):
        TestHelperObject = TestHelper()
        with self.assertRaises(KeyError):
            self.LambdaServiceObject.archive_create(
                function_name=TestHelperObject.function_name,
                mute=True
            )


if __name__ == '__main__':
    unittest.main()
