import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs
from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class TestFunctionNameSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_function_name_set_success(self):
        self.LambdaArgsObject.function_name_set(DEFAULT_TEST_LAMBDA_NAME)
        self.assertEqual(self.LambdaArgsObject.function, DEFAULT_TEST_LAMBDA_NAME)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
