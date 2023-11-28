import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestUpdateFunctionCode(unittest.TestCase):

    function_name = None
    parser = None
    CreateCommandObject = None
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

        cls.LambdaServiceObject = LambdaService(verbose=False)

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_update_function_code_success_with_code_changed(self):
        self.TestHelperObject.create_tests_files(self.function_name)
        self.LambdaServiceObject.archive_create(
            function_name=self.function_name,
            mute=True
        )
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_update_function_code_success',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        self.TestHelperObject.update_tests_lambda_file(self.function_name)
        try:
            response = self.LambdaServiceObject.lambda_update_code(
                function_name=self.function_name,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        finally:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )
            self.TestHelperObject.remove_tests_folder()
        self.assertTrue(response)

    def test_update_function_code_success_without_code_changed(self):
        self.TestHelperObject.create_tests_files(self.function_name)
        self.LambdaServiceObject.archive_create(
            function_name=self.function_name,
            mute=True
        )
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_update_function_code_success',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        try:
            response = self.LambdaServiceObject.lambda_update_code(
                function_name=self.function_name,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        finally:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )
            self.TestHelperObject.remove_tests_folder()
        self.assertTrue(response)

    # test errors
    def test_update_function_code_error_input_invalid_type_function_name(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_update_code(
                function_name={'function_name': self.function_name},
                mute=True
            )

    def test_update_function_code_error_input_invalid_type_mute(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_update_code(
                function_name=self.function_name,
                mute={'mute': True}
            )

    def test_update_function_code_error_function_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.LambdaServiceObject.lambda_update_code(
                function_name=self.function_name,
                mute=True
            )

    def test_update_function_code_error_botocore_function_not_found(self):
        self.TestHelperObject.create_tests_files(self.function_name)
        self.LambdaServiceObject.archive_create(
            function_name=self.function_name,
            mute=True
        )
        with self.assertRaises(self.LambdaServiceObject.client.exceptions.ResourceNotFoundException):
            self.LambdaServiceObject.lambda_update_code(
                function_name=self.function_name,
                mute=True
            )
        self.TestHelperObject.remove_tests_folder()


if __name__ == '__main__':
    unittest.main()
