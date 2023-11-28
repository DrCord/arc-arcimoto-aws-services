import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs
from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class Test_SetAttributesFromKwargs(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()
    test_input = {
        'function_name': DEFAULT_TEST_LAMBDA_NAME
    }

    # test successes
    def test__set_attributes_from_kwargs_success(self):
        self.LambdaArgsObject._set_attributes_from_kwargs(self.test_input)
        self.assertEqual(self.LambdaArgsObject.function_name, DEFAULT_TEST_LAMBDA_NAME)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
