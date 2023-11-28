from copy import deepcopy
import tempfile
import unittest
import warnings

from arcimoto_aws_services import bundle
from tests.dependencies import DependenciesConfigFile
from .bundle import TestBundle
from tests.TestHelper import TestHelper


class TestAssembleAssets(unittest.TestCase, TestBundle):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning,
            message='unclosed.*<ssl.SSLSocket.*>'
        )
        cls.DependenciesFileObject = DependenciesConfigFile()
        cls.DependenciesFileObject.dependencies_create_file()

        cls.TestHelperObject = TestHelper()
        cls.TestHelperObject.create_tests_files()

        cls.build_dir = tempfile.TemporaryDirectory()

        (cls.functions, cls.common_config, cls.global_dependencies) = bundle.load_dependencies()
        cls.function_config = cls.functions.get(cls.function_name, None)
        cls.assets = bundle.assets_for_function(cls.function_name, cls.function_config, cls.common_config)

    @classmethod
    def tearDownClass(cls):
        cls.DependenciesFileObject.dependencies_remove_file()
        cls.build_dir.cleanup()
        cls.TestHelperObject.remove_tests_folder()

    # test successes
    def test_assemble_assets_success(self):
        try:
            bundle.assemble_assets(self.assets, self.build_dir.name)
        except Exception as e:
            self.fail(f'assemble_assets failed: {e}')

    def test_assemble_assets_success_layer(self):
        assets = deepcopy(self.assets)
        for asset in assets:
            asset['name'] = 'assemble_assets'
        try:
            bundle.assemble_assets(assets, self.build_dir.name, True)
        except Exception as e:
            self.fail(f'assemble_assets [layer=True] failed: {e}')

    # test errors
    def test_assemble_assets_error_asset_invalid_action(self):
        assets = deepcopy(self.assets)
        invalid_asset = {
            'action': 'not-a-valid-action'
        }
        assets.append(invalid_asset)
        with self.assertRaises(ValueError):
            bundle.assemble_assets(assets, self.build_dir.name)

    def test_assemble_assets_error_asset_source_missing(self):
        assets = deepcopy(self.assets)
        invalid_asset = {
            'action': 'copy'
        }
        assets.append(invalid_asset)
        with self.assertRaises(ValueError):
            bundle.assemble_assets(assets, self.build_dir.name)

    def test_assemble_assets_error_asset_missing_destination_when_layer_false(self):
        assets = deepcopy(self.assets)
        invalid_asset = {
            'action': 'copy',
            'from': 'magic'
        }
        assets.append(invalid_asset)
        with self.assertRaises(ValueError):
            bundle.assemble_assets(assets, self.build_dir.name)

    def test_assemble_assets_error_asset_missing_name_when_layer_true(self):
        assets = deepcopy(self.assets)
        invalid_asset = {
            'action': 'copy',
            'from': 'magic'
        }
        assets.append(invalid_asset)
        with self.assertRaises(ValueError):
            bundle.assemble_assets(assets, self.build_dir.name, True)


if __name__ == '__main__':
    unittest.main()
