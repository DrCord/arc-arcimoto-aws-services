from botocore.exceptions import ParamValidationError
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


class Test_LayerPublishVersion(unittest.TestCase):

    args = None

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

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestLambdaLayersServiceObject.archive_remove()

    # test successes
    def test__layer_publish_version_success(self):
        LambdaLayersServiceObject = LambdaLayersService(
            DEFAULT_TEST_LAMBDA_LAYER_NAME
        )
        LambdaLayersServiceObject._layer_description_set()
        LambdaLayersServiceObject._archive_create()
        try:
            LambdaLayersServiceObject._layer_publish_version(
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    def test__layer_publish_version_error_input_invalid_type_mute(self):
        LambdaLayersServiceObject = LambdaLayersService(
            DEFAULT_TEST_LAMBDA_LAYER_NAME
        )
        LambdaLayersServiceObject._layer_description_set()
        LambdaLayersServiceObject._archive_create()
        with self.assertRaises(ValueError):
            LambdaLayersServiceObject._layer_publish_version(
                mute={'mute': False}
            )

    def test__layer_publish_version_error_botocore_input_invalid_type_Description(self):
        LambdaLayersServiceObject = LambdaLayersService(
            DEFAULT_TEST_LAMBDA_LAYER_NAME
        )
        LambdaLayersServiceObject._archive_create()
        with self.assertRaises(ParamValidationError):
            LambdaLayersServiceObject._layer_publish_version(
                mute=True
            )

    def test__layer_publish_version_error_botocore_input_invalid_type_LayerName(self):
        LambdaLayersServiceObject = LambdaLayersService(
            DEFAULT_TEST_LAMBDA_LAYER_NAME
        )
        LambdaLayersServiceObject._layer_description_set()
        LambdaLayersServiceObject._archive_create()
        LambdaLayersServiceObject.layer_name = None
        with self.assertRaises(ParamValidationError):
            LambdaLayersServiceObject._layer_publish_version(
                mute=True
            )

    def test__layer_publish_version_error_botocore_input_invalid_type_ZipFile(self):
        LambdaLayersServiceObject = LambdaLayersService(
            DEFAULT_TEST_LAMBDA_LAYER_NAME
        )
        LambdaLayersServiceObject._layer_description_set(self.args.description)
        with self.assertRaises(ParamValidationError):
            LambdaLayersServiceObject._layer_publish_version(
                mute=True
            )


if __name__ == '__main__':
    unittest.main()
