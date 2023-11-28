import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaLayersService

from tests.dependencies import DependenciesConfigFile

from tests.lambda_service.lambda_layers_service.lambda_layers_service import (
    DEFAULT_TEST_LAMBDA_LAYER_NAME,
    TestLambdaLayersService
)


class Test_LayerDescriptionSet(unittest.TestCase, TestLambdaLayersService):

    args = None
    global_dependencies_default_description = 'contains: [common_dependency1, common_dependency2]'
    global_dependencies_default_description_addendum = ', description: from arcimoto_lambda_utility test creation'
    LambdaLayersServiceObject = None

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

        cls.LambdaLayersServiceObject = LambdaLayersService(
            DEFAULT_TEST_LAMBDA_LAYER_NAME
        )

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestLambdaLayersServiceObject.archive_remove()

    # test successes
    def test__layer_description_set_success_no_input(self):
        try:
            self.LambdaLayersServiceObject._layer_description_set()
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertEqual(
            self.LambdaLayersServiceObject.layer_description,
            self.global_dependencies_default_description
        )

    def test__layer_description_set_success_with_input(self):
        global_dependencies_custom_description_addendum = 'description addendum test string'
        try:
            self.LambdaLayersServiceObject._layer_description_set(global_dependencies_custom_description_addendum)
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertEqual(
            self.LambdaLayersServiceObject.layer_description,
            f'{self.global_dependencies_default_description}, description: {global_dependencies_custom_description_addendum}'
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
