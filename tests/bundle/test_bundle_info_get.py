import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle
from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class TestBundleInfoGet(unittest.TestCase, TestBundle):

    function_name = DEFAULT_TEST_LAMBDA_NAME
    lambda_bundle_name = None
    bundle_json_file_path = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning,
            message='unclosed.*<ssl.SSLSocket.*>'
        )
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()
        cls.lambda_bundle_name = bundle.lambda_bundle_get(cls.function_name)
        cls.bundle_json_file_path = f'lambda/{cls.lambda_bundle_name}/bundle.json'
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_bundle_info_get_success(self):
        try:
            bundle.bundle_info_get(self.function_name, self.lambda_bundle_name, self.bundle_json_file_path, True)
        except Exception as e:
            self.fail(f'bundle_info_get failed: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
