import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestAddLayers(unittest.TestCase):

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
    def test_add_layers_success(self):
        self.LambdaServiceObject.archive_create(
            function_name=self.function_name,
            mute=True
        )
        self.LambdaServiceObject.create(
            function_name=self.function_name,
            description='test_add_layers_success',
            zip_bytes=self.LambdaServiceObject.zip_bytes,
            role=self.TestHelperObject.role,
            mute=True
        )
        try:
            self.LambdaServiceObject.add_layers(
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

    # test errors
    def test_add_layers_error_input_function_name_missing(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.add_layers(
                mute=True
            )

    def test_add_layers_error_input_function_name_null(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.add_layers(
                function_name=None,
                mute=True
            )

    def test_add_layers_error_input_mute_type_invalid(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.add_layers(
                function_name=self.function_name,
                mute='not-a-Boolean'
            )

    def test_add_layers_error_input_function_name_no_configuration_found(self):
        TestHelperObject = TestHelper()
        with self.assertRaises(KeyError):
            self.LambdaServiceObject.add_layers(
                function_name=TestHelperObject.function_name,
                mute=True
            )


if __name__ == '__main__':
    unittest.main()
