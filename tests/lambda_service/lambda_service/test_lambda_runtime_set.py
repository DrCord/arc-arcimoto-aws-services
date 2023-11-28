from time import sleep
import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestLambdaRuntimeSet(unittest.TestCase):

    arn = None
    function_name = None
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
        cls.LambdaServiceObject.archive_create(
            function_name=cls.function_name,
            mute=True
        )
        cls.arn = cls.LambdaServiceObject.create(
            function_name=cls.function_name,
            description='default description from unit tests',
            zip_bytes=cls.LambdaServiceObject.zip_bytes,
            role=cls.TestHelperObject.role,
            mute=True
        )
        cls.LambdaServiceObject.lambda_dev_alias_create(
            function_name=cls.function_name,
            mute=True
        )

    @classmethod
    def tearDownClass(cls):
        if cls.arn is not None:
            cls.LambdaServiceObject.delete(
                function_name=cls.function_name,
                mute=True
            )
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestHelperObject.remove_tests_folder()

    # test successes
    def test_lambda_runtime_set_success(self):
        invoked = False
        count = 0
        fail_count = 10
        while not invoked and count < fail_count:
            sleep(5)
            try:
                self.LambdaServiceObject.lambda_runtime_set(
                    function_name=self.function_name,
                    mute=True
                )
                invoked = True
            except self.LambdaServiceObject.client.exceptions.ResourceConflictException as e:
                # lambda not ready to invoke yet
                count += 1
                if not invoked and count == fail_count:
                    self.fail(f'Unable to invoke function: {e}')
                continue
            except Exception as e:
                self.fail(f'test failed unexpectedly: {e}')

    # test errors
    def test_lambda_runtime_set_error_input_function_name_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_runtime_set(
                function_name={'function_name': 'a-dictionary-is-not-a-string'},
                mute=True
            )

    def test_lambda_runtime_set_error_input_mute_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_runtime_set(
                function_name=self.function_name,
                mute='not-a-Boolean'
            )

    def test_lambda_runtime_set_error_input_verbose_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_runtime_set(
                function_name=self.function_name,
                mute=True,
                verbose='not-a-Boolean'
            )

    def test_lambda_runtime_set_error_input_python3_minor_version_not_in_allowed_values(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_runtime_set(
                function_name=self.function_name,
                python3_minor_version='not-allowed',
                mute=True
            )


if __name__ == '__main__':
    unittest.main()
