import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestDelete(unittest.TestCase):

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
    def test_delete_success(self):
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_delete_success',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        try:
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    def test_delete_error_input_function_name_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.delete(
                function_name=1234567890,
                mute=True
            )

    def test_delete_error_input_mute_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                mute='not a Boolean'
            )

    def test_delete_error_input_verbose_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.delete(
                function_name=self.function_name,
                verbose='not-a-Boolean',
                mute=True
            )


if __name__ == '__main__':
    unittest.main()
