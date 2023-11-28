import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaLayersService

from tests.dependencies import DependenciesConfigFile

from tests.lambda_service.lambda_layers_service.lambda_layers_service import (
    DEFAULT_TEST_LAMBDA_LAYER_NAME,
    TestLambdaLayersService
)


class Test_LayerConfigGet(unittest.TestCase):

    args = None
    DependenciesFileObject = None
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
    def test__layer_config_get_success(self):
        try:
            LambdaLayersServiceObject = LambdaLayersService(DEFAULT_TEST_LAMBDA_LAYER_NAME)
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertEqual(LambdaLayersServiceObject.layer_identifier, DEFAULT_TEST_LAMBDA_LAYER_NAME)
        self.assertIsNotNone(LambdaLayersServiceObject.layer_config)
        self.assertIsNotNone(LambdaLayersServiceObject.layer_name)
        # empty list of packages would evaluate to false
        self.assertTrue(LambdaLayersServiceObject.layer_packages)

    # test errors
    def test__layer_config_get_error_layer_configuration_not_found(self):
        with self.assertRaises(KeyError):
            LambdaLayersService(f'{DEFAULT_TEST_LAMBDA_LAYER_NAME}-not-real')

    def test__layer_config_get_error_layer_configuration_no_name(self):
        with self.assertRaises(KeyError):
            LambdaLayersService('package2-missing-name-property')


if __name__ == '__main__':
    unittest.main()
