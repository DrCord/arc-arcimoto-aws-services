import unittest
import warnings

from arcimoto_aws_services.lambda_service import (
    DEV_ALIAS,
    STAGING_ALIAS,
    LambdaService
)

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestLambdaAliasUpdate(unittest.TestCase):

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

        cls.TestHelperObject.create_tests_files(cls.function_name)

        cls.LambdaServiceObject = LambdaService(verbose=False)
        cls.LambdaServiceObject.archive_create(
            function_name=cls.function_name,
            mute=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestHelperObject.remove_tests_folder()

    # test successes
    def test_lambda_alias_update_success(self):
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_lambda_alias_update_success',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        self.LambdaServiceObject.lambda_dev_alias_create(
            function_name=self.function_name,
            mute=True
        )
        version = self.LambdaServiceObject.lambda_publish_version(
            function_name=self.function_name,
            mute=True
        )
        self.LambdaServiceObject.lambda_alias_create(
            function_name=self.function_name,
            alias=STAGING_ALIAS,
            version=version,
            mute=True
        )
        try:
            response = self.LambdaServiceObject.lambda_alias_update(
                function_name=self.function_name,
                alias=STAGING_ALIAS,
                version=version,
                description='unit test created',
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        finally:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )
        self.assertIsInstance(response, dict)

    # test errors
    def test_lambda_alias_update_error_input_invalid_type_function_name(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_alias_update(
                function_name={'function_name': self.function_name},
                alias=STAGING_ALIAS,
                version='1',
                description='unit test created',
                mute=True
            )

    def test_lambda_alias_update_error_input_invalid_env_not_in_allowed_values(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_alias_update(
                function_name=self.function_name,
                alias='not-a-real-env',
                version='1',
                description='unit test created',
                mute=True
            )

    def test_lambda_alias_update_error_input_invalid_type_description(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_alias_update(
                function_name=self.function_name,
                alias=STAGING_ALIAS,
                version='1',
                description={'description': 'unit test created'},
                mute=True
            )

    def test_lambda_alias_update_error_input_invalid_type_mute(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_alias_update(
                function_name=self.function_name,
                alias=DEV_ALIAS,
                mute={'mute': True}
            )

    def test_lambda_alias_update_error_botocore_function_not_found(self):
        with self.assertRaises(self.LambdaServiceObject.client.exceptions.ResourceNotFoundException):
            self.LambdaServiceObject.lambda_alias_update(
                function_name=self.function_name,
                alias=STAGING_ALIAS,
                version='1',
                description='unit test created',
                mute=True
            )

    def test_lambda_alias_update_error_botocore_function_version_not_found(self):
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_lambda_alias_update_success',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        with self.assertRaises(self.LambdaServiceObject.client.exceptions.ResourceNotFoundException):
            self.LambdaServiceObject.lambda_alias_update(
                function_name=self.function_name,
                alias=STAGING_ALIAS,
                version='1',
                description='unit test created',
                mute=True
            )
        self.LambdaServiceObject.delete(
            function_name=self.function_name,
            mute=True
        )


if __name__ == '__main__':
    unittest.main()
