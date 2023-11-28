import unittest
import warnings

from arcimoto_aws_services.lambda_service import (
    DEV_ALIAS,
    LambdaService
)

from tests.dependencies import DependenciesConfigFile
from tests.TestHelper import TestHelper


class TestListLayerVersions(unittest.TestCase):

    arn = None
    function_name = None
    LambdaServiceObject = None
    TestHelperObject = None

    global_dependencies_dev_layer_name = f'arcimoto-globals-{DEV_ALIAS}'

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
        cls.arn = cls.LambdaServiceObject.create(
            function_name=cls.function_name,
            description='test_list_layer_versions',
            zip_bytes=cls.LambdaServiceObject.zip_bytes,
            role=cls.TestHelperObject.role,
            mute=True
        )

    @classmethod
    def tearDownClass(cls):
        if cls.arn is not None:
            cls.LambdaServiceObject.delete(
                function_name=cls.function_name,
                mute=True
            )
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.TestHelperObject.remove_tests_folder()

    # test successes
    def test_list_layer_versions_success(self):
        try:
            self.LambdaServiceObject.list_layer_versions(
                self.global_dependencies_dev_layer_name,
                False,
                True
            )
        except Exception as e:
            self.fail(f'create.lambda_create failed unexpectedly: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
