import unittest
import warnings

from arcimoto_aws_services.aws_service import (
    DEFAULT_AWS_ACCOUNT_ID,
    DEFAULT_AWS_REGION
)
from arcimoto_aws_services.lambda_service import LambdaApiGatewayService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper

from tests.constants import (
    DEFAULT_TEST_API_ID,
    DEFAULT_TEST_API_PATH,
    DEFAULT_TEST_LAMBDA_ENV
)


class TestPolicyExists(unittest.TestCase):

    api_arn = None
    default_description = 'Unit test created'
    lambda_arn = None
    LambdaServiceObject = None

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

        cls.LambdaServiceObject = LambdaApiGatewayService(
            verbose=False
        )
        cls.LambdaServiceObject.archive_create(
            function_name=cls.function_name,
            mute=True
        )
        cls.lambda_arn = cls.LambdaServiceObject.lambda_arn_build(
            DEFAULT_AWS_REGION,
            DEFAULT_AWS_ACCOUNT_ID,
            cls.function_name,
            DEFAULT_TEST_LAMBDA_ENV
        )
        cls.api_arn = cls.LambdaServiceObject.api_arn_build(
            DEFAULT_AWS_REGION,
            DEFAULT_AWS_ACCOUNT_ID,
            DEFAULT_TEST_API_ID,
            DEFAULT_TEST_API_PATH
        )

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestHelperObject.remove_tests_folder()

    # test successes
    def test_policy_exists_success_policy_exists(self):
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description=self.default_description,
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        self.LambdaServiceObject.lambda_dev_alias_create(
            function_name=self.function_name,
            mute=True
        )
        self.LambdaServiceObject.policy_deploy(
            api_arn=self.api_arn,
            lambda_arn=self.lambda_arn,
            mute=True
        )
        try:
            policy_exists = self.LambdaServiceObject.policy_exists(
                lambda_arn=self.lambda_arn,
                api_arn=self.api_arn,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        finally:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )
        self.assertTrue(policy_exists)

    def test_policy_exists_success_policy_does_not_exist(self):
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description=self.default_description,
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        self.LambdaServiceObject.lambda_dev_alias_create(
            function_name=self.function_name,
            mute=True
        )
        try:
            policy_exists = self.LambdaServiceObject.policy_exists(
                lambda_arn=self.lambda_arn,
                api_arn=self.api_arn,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        finally:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )
        self.assertFalse(policy_exists)

    # test errors
    def test_policy_exists_error_input_api_arn_invalid_type(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.policy_exists(
                api_arn={'api_arn': 'dict-is-not-a-string'},
                lambda_arn=self.lambda_arn,
                mute=True
            )

    def test_policy_exists_error_input_lambda_arn_invalid_type(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.policy_exists(
                api_arn=self.api_arn,
                lambda_arn={'lambda_arn': 'dict-is-not-a-string'},
                mute=True
            )

    def test_policy_exists_error_input_mute_invalid_type(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.policy_exists(
                api_arn=self.api_arn,
                lambda_arn=self.lambda_arn,
                mute='not-a-boolean'
            )


if __name__ == '__main__':
    unittest.main()
