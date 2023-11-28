import unittest
import warnings

from arcimoto_aws_services.lambda_service import (
    DEV_ALIAS,
    LambdaService
)

from tests.dependencies import DependenciesConfigFile


class TestGetLatestLayer(unittest.TestCase):

    DependenciesFileObject = None
    LambdaServiceObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()

        cls.LambdaServiceObject = LambdaService(verbose=False)

        cls.global_dependencies_layer_name = 'arcimoto-globals'
        cls.global_dependencies_dev_layer_name = f'{cls.global_dependencies_layer_name}-{DEV_ALIAS}'

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_get_latest_layer_success(self):
        try:
            self.LambdaServiceObject.get_latest_layer(
                self.global_dependencies_dev_layer_name,
                False,
                True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    def test_get_latest_layer_error_input_layer_name_not_found(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.get_latest_layer(
                f'{self.global_dependencies_dev_layer_name}-not-real-layer',
                False,
                True
            )


if __name__ == '__main__':
    unittest.main()
