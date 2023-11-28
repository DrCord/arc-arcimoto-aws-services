import unittest
import warnings

from arcimoto_aws_services.lambda_service import (
    DEV_ALIAS,
    LambdaService
)

from tests.dependencies import DependenciesConfigFile


class TestGetLatestGlobalDependenciesLayerVersion(unittest.TestCase):

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

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_get_latest_global_dependencies_layer_version_success_no_input(self):
        try:
            latest_global_dependencies_layer_version = self.LambdaServiceObject.get_latest_global_dependencies_layer_version()
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertIsInstance(latest_global_dependencies_layer_version, int)

    def test_get_latest_global_dependencies_layer_version_success_input_env(self):
        try:
            self.LambdaServiceObject.get_latest_global_dependencies_layer_version(DEV_ALIAS)
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    def test_get_latest_global_dependencies_layer_version_error_input_env_not_in_allowed_values(self):
        with self.assertRaises(ValueError):
            self.LambdaServiceObject.get_latest_global_dependencies_layer_version(f'{DEV_ALIAS}-not-real-alias')


if __name__ == '__main__':
    unittest.main()
