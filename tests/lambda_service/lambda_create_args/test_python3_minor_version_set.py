import unittest

from arcimoto_aws_services.lambda_service import (
    PYTHON3_MINOR_VERSION_DEFAULT,
    LambdaCreateArgs
)


class TestPython3MinorVersionSet(unittest.TestCase):

    LambdaArgsObject = LambdaCreateArgs()

    # test successes
    def test_python3_minor_version_set_success_no_input(self):
        self.LambdaArgsObject.python3_minor_version_set()
        self.assertEqual(self.LambdaArgsObject.python3_minor_version, PYTHON3_MINOR_VERSION_DEFAULT)

    def test_python3_minor_version_set_success_input(self):
        self.LambdaArgsObject.python3_minor_version_set(PYTHON3_MINOR_VERSION_DEFAULT)
        self.assertEqual(self.LambdaArgsObject.python3_minor_version, PYTHON3_MINOR_VERSION_DEFAULT)

    # test errors
    def test_python3_minor_version_set_error_input_not_in_allowed_versions(self):
        with self.assertRaises(ValueError):
            self.LambdaArgsObject.python3_minor_version_set(12345)


if __name__ == '__main__':
    unittest.main()
