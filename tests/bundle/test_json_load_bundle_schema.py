import json
import unittest
import warnings

from arcimoto_aws_services import bundle

from .bundle import TestBundle
from tests.bundles import TestBundles


class TestJsonLoadBundleSchema(unittest.TestCase, TestBundle):

    TestBundlesObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

        cls.TestBundlesObject = TestBundles()

    # test successes
    def test_json_load_bundle_schema_success(self):
        self.TestBundlesObject.bundle_schema_file_create()
        try:
            bundle.json_load_bundle_schema()
        except Exception as e:
            self.fail(f'json_load_bundle_schema failed: {e}')
        finally:
            self.TestBundlesObject.bundle_schema_file_remove()

    # test errors
    def test_json_load_bundle_schema_error_bundle_name_file_path_not_found(self):
        with self.assertRaises(FileNotFoundError):
            bundle.json_load_bundle_schema()

    def test_json_load_bundle_schema_error_file_contains_invalid_json(self):
        self.TestBundlesObject.bundle_schema_invalid_file_create()
        with self.assertRaises(json.decoder.JSONDecodeError):
            bundle.json_load_bundle_schema()
        self.TestBundlesObject.bundle_schema_invalid_file_remove()


if __name__ == '__main__':
    unittest.main()
