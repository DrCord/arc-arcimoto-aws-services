import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestCreate(unittest.TestCase):

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
    def test_create_success(self):
        try:
            arn = self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_success',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
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
    # missing/invalid input
    def test_create_error_input_function_name_missing(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                mute=True
            )

    def test_create_error_input_function_name_null(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=None,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                mute=True
            )

    def test_create_error_input_description_missing(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                mute=True
            )

    def test_create_error_input_description_null(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description=None,
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                mute=True
            )

    def test_create_error_input_zip_bytes_null(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=None,
                role=self.TestHelperObject.role,
                mute=True
            )

    def test_create_error_input_role_missing(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                mute=True
            )

    def test_create_error_input_role_null(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=None,
                mute=True
            )

    def test_create_error_input_vpc_not_in_allowed_values(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                vpc='not-an-arcimoto-vpc-name',
                mute=True
            )

    def test_create_error_input_timeout_not_positive_integer(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                timeout=-1,
                mute=True
            )

    def test_create_error_input_tags_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                tags='not a dictionary',
                mute=True
            )

    def test_create_error_input_verbose_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                verbose='not a Boolean',
                mute=True
            )

    def test_create_error_input_mute_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                verbose=False,
                mute='not a Boolean'
            )

    def test_create_error_function_name_exists(self):
        arn = self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_create_error',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        try:
            self.LambdaServiceObject.create(
                function_name=self.function_name,
                description='test_create_error',
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                mute=True
            )
        except Exception as e:
            self.fail(f'create failed expectedly: {e}')

        if arn is not None:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )

    def test_create_error_function_configuration_not_found(self):
        TestHelperObject = TestHelper()
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.create(
                function_name=TestHelperObject.function_name,
                description=None,
                zip_bytes=self.LambdaServiceObject.zip_bytes,
                role=self.TestHelperObject.role,
                mute=True
            )


if __name__ == '__main__':
    unittest.main()
