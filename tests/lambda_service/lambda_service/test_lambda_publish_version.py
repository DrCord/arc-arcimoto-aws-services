import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestLambdaPublishVersion(unittest.TestCase):

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
    def test_lambda_publish_version_success(self):
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_lambda_publish_version_success',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        try:
            response = self.LambdaServiceObject.lambda_publish_version(
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
        self.assertIsInstance(response, str)
        self.assertGreaterEqual(int(response), 1)

    # test errors
    def test_lambda_publish_version_error_input_invalid_type_function_name(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_publish_version(
                function_name={'function_name': self.function_name},
                mute=True
            )

    def test_lambda_publish_version_error_input_invalid_type_verbose(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_publish_version(
                function_name=self.function_name,
                verbose={'verbose': True},
                mute=True
            )

    def test_lambda_publish_version_error_input_invalid_type_mute(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.lambda_publish_version(
                function_name=self.function_name,
                mute={'mute': True}
            )


if __name__ == '__main__':
    unittest.main()
