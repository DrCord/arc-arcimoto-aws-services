import unittest

from arcimoto_aws_services.lambda_service import (
    PYTHON3_MINOR_VERSION_DEFAULT,
    LambdaRuntimeArgs
)


class Test_Python3MinorVersionSet(unittest.TestCase):

    LambdaArgsObject = LambdaRuntimeArgs()

    # test successes
    def test_python3_minor_version_set_success(self):
        self.LambdaArgsObject._python3_minor_version_set()
        self.assertEqual(self.LambdaArgsObject.python3_minor_version, PYTHON3_MINOR_VERSION_DEFAULT)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
