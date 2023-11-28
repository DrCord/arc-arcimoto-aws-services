from copy import deepcopy
import unittest
import warnings

from arcimoto_aws_services import bundle

from tests.dependencies import DependenciesConfigFile
from tests.constants import DEFAULT_TEST_LAMBDA_NAME
from .bundle import TestBundle


class TestAssetsForFunction(unittest.TestCase, TestBundle):

    function_config = None
    function_name = DEFAULT_TEST_LAMBDA_NAME
    functions = None
    common_config = None
    global_dependencies = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning,
            message='unclosed.*<ssl.SSLSocket.*>'
        )
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()
        (cls.functions, cls.common_config, cls.global_dependencies) = bundle.load_dependencies()
        cls.function_config = cls.functions.get(cls.function_name, None)
        cls.DependenciesFileObject.dependencies_remove_file()

    # test successes
    def test_assets_for_function_success(self):
        try:
            bundle.assets_for_function(self.function_name, self.function_config, self.common_config)
        except Exception as e:
            self.fail(f'assets_for_function failed: {e}')

    # test errors
    def test_copy_asset_error_function_name_null(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(None, self.function_config, self.common_config)

    def test_copy_asset_error_function_config_null(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(self.function_name, None, self.common_config)

    def test_copy_asset_error_common_config_null(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(self.function_name, self.function_config, None)

    def test_copy_asset_error_function_name_type_invalid(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(1, self.function_config, self.common_config)

    def test_copy_asset_error_function_config_type_invalid(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(self.function_name, 'not a dictionary', self.common_config)

    def test_copy_asset_error_common_config_type_invalid(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(self.function_name, self.function_config, 'not a dictionary')

    def test_copy_asset_error_function_config_empty(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(self.function_name, {}, self.common_config)

    def test_copy_asset_error_common_config_empty(self):
        with self.assertRaises(ValueError):
            bundle.assets_for_function(self.function_name, self.function_config, {})

    def test_copy_asset_error_function_config_has_undefined_common_dependency(self):
        function_config = deepcopy(self.function_config)
        function_config['common_dependencies'] = ['not-a-real-common-dependency']
        with self.assertRaises(KeyError):
            bundle.assets_for_function(self.function_name, function_config, self.common_config)

    def test_copy_asset_error_function_config_has_null_bundle(self):
        function_config = deepcopy(self.function_config)
        function_config['bundle'] = None
        with self.assertRaises(ValueError):
            bundle.assets_for_function(self.function_name, function_config, self.common_config)


if __name__ == '__main__':
    unittest.main()
