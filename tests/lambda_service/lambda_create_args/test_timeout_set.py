import unittest

from arcimoto_aws_services.lambda_service import (
    LAMBDA_DEFAULT_TIMEOUT,
    LambdaCreateArgs
)


class TestTimeoutSet(unittest.TestCase):

    LambdaArgsObject = LambdaCreateArgs()

    # test successes
    def test_timeout_set_success_no_input(self):
        self.LambdaArgsObject.timeout_set()
        self.assertEqual(self.LambdaArgsObject.timeout, LAMBDA_DEFAULT_TIMEOUT)

    def test_timeout_set_success_input(self):
        self.LambdaArgsObject.timeout_set(LAMBDA_DEFAULT_TIMEOUT)
        self.assertEqual(self.LambdaArgsObject.timeout, LAMBDA_DEFAULT_TIMEOUT)

    # test errors
    def test_timeout_set_error_input_not_positive_integer(self):
        with self.assertRaises(ValueError):
            self.LambdaArgsObject.timeout_set(-1)


if __name__ == '__main__':
    unittest.main()
