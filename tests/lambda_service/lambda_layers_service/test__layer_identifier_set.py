import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaLayersService

from tests.dependencies import DependenciesConfigFile

from tests.lambda_service.lambda_layers_service.lambda_layers_service import (
    DEFAULT_TEST_LAMBDA_LAYER_NAME,
    TestLambdaLayersService
)


class Test_LayerIdentifierSet(unittest.TestCase):

    args = None
    TestLambdaLayersServiceObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()
        cls.TestLambdaLayersServiceObject = TestLambdaLayersService()

        cls.TestLambdaLayersServiceObject.archive_create()

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestLambdaLayersServiceObject.archive_remove()

    # test successes
    def test__layer_identifier_set_success(self):
        try:
            LambdaLayersServiceObject = LambdaLayersService(DEFAULT_TEST_LAMBDA_LAYER_NAME)
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertEqual(LambdaLayersServiceObject.layer_identifier, DEFAULT_TEST_LAMBDA_LAYER_NAME)

    # test errors
    def test__layer_identifier_set_error_input_layer_identifier_invalid_type(self):
        with self.assertRaises(ValueError):
            LambdaLayersService({'layer_identifier': DEFAULT_TEST_LAMBDA_LAYER_NAME})


if __name__ == '__main__':
    unittest.main()
