import unittest
import warnings

from arcimoto_aws_services.lambda_service import (
    LambdaLayersArgs,
    LambdaLayersService
)

from tests.dependencies import DependenciesConfigFile

from tests.lambda_service.lambda_layers_service.lambda_layers_service import (
    DEFAULT_TEST_LAMBDA_LAYER_NAME,
    TestLambdaLayersService
)


class TestPublishLayerVersion(unittest.TestCase):

    args = None
    LambdaLayersServiceObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

        cls.args = LambdaLayersArgs()

        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()
        cls.TestLambdaLayersServiceObject = TestLambdaLayersService()

        cls.TestLambdaLayersServiceObject.archive_create()

        cls.LambdaLayersServiceObject = LambdaLayersService(
            DEFAULT_TEST_LAMBDA_LAYER_NAME
        )

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestLambdaLayersServiceObject.archive_remove()

    # test successes
    def test__layer_publish_version_success(self):
        try:
            self.LambdaLayersServiceObject.publish_layer_version(
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
