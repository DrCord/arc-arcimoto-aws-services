import unittest
import warnings

from arcimoto_aws_services.lambda_service import (
    DEV_ALIAS,
    STAGING_ALIAS,
    LambdaService
)

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestLambdaAliasCreate(unittest.TestCase):

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
            description='test_lambda_alias_create',
            zip_bytes=cls.LambdaServiceObject.zip_bytes,
            role=cls.TestHelperObject.role,
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
    def test_lambda_alias_create_success_no_input_alias(self):
        # we have to explictly delete any existing unit test lambdas
        # as this was coliding even when created in separate tests
        self.LambdaServiceObject.delete(
            function_name=self.function_name,
            mute=True
        )
        arn = self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_lambda_alias_create',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        try:
            self.LambdaServiceObject.lambda_alias_create(
                function_name=self.function_name,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        finally:
            if arn is not None:
                self.LambdaServiceObject.delete(
                    function_name=self.function_name,
                    mute=True
                )

    def test_lambda_alias_create_success_input_alias(self):
        # we have to explictly delete any existing unit test lambdas
        # as this was coliding even when created in separate tests
        self.LambdaServiceObject.delete(
            function_name=self.function_name,
            mute=True
        )
        arn = self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_lambda_alias_create',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        self.LambdaServiceObject.lambda_alias_create(
            function_name=self.function_name,
            mute=True
        )
        version = self.LambdaServiceObject.lambda_alias_latest_version_get(
            function_name=self.function_name,
            mute=False
        )
        try:
            self.LambdaServiceObject.lambda_alias_create(
                function_name=self.function_name,
                alias=STAGING_ALIAS,
                version=version,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        finally:
            if arn is not None:
                self.LambdaServiceObject.delete(
                    function_name=self.function_name,
                    mute=True
                )

    # test errors
    def test_lambda_create_error_input_function_name_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_alias_create(
                function_name=1234567890,
                mute=True
            )

    def test_lambda_create_error_input_alias_not_in_allowed_values(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_alias_create(
                function_name=self.function_name,
                alias=f'{DEV_ALIAS}-not-a-real-alias',
                mute=True
            )

    def test_lambda_create_error_input_function_name_not_found(self):
        TestHelperObject = TestHelper()
        with self.assertRaises(self.LambdaServiceObject.client.exceptions.ResourceNotFoundException):
            self.LambdaServiceObject.lambda_alias_create(
                function_name=TestHelperObject.function_name,
                mute=True
            )

    def test_lambda_alias_create_error_alias_already_exists(self):
        arn = self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_lambda_alias_create',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        self.LambdaServiceObject.lambda_alias_create(
            function_name=self.function_name,
            mute=True
        )
        with self.assertRaises(self.LambdaServiceObject.client.exceptions.ResourceConflictException):
            self.LambdaServiceObject.lambda_alias_create(
                function_name=self.function_name,
                mute=True
            )
        if arn is not None:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )


if __name__ == '__main__':
    unittest.main()
