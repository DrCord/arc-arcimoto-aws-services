import unittest

from arcimoto_aws_services.lambda_service import LambdaLayersService

from tests.dependencies import DependenciesConfigFile

from tests.lambda_service.lambda_layers_service.lambda_layers_service import DEFAULT_TEST_LAMBDA_LAYER_NAME


class Test__init(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_init_success(self):
        try:
            LambdaLayersServiceObject = LambdaLayersService(
                DEFAULT_TEST_LAMBDA_LAYER_NAME
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertEqual(LambdaLayersServiceObject.layer_identifier, DEFAULT_TEST_LAMBDA_LAYER_NAME)
        self.assertIsNotNone(LambdaLayersServiceObject.layer_config)
        self.assertIsNotNone(LambdaLayersServiceObject.layer_name)
        # empty list of packages would evaluate to false
        self.assertTrue(LambdaLayersServiceObject.layer_packages)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
