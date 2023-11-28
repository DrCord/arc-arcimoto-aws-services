import unittest

from arcimoto_aws_services.lambda_service import (
    LAMBDA_DEFAULT_VPC,
    LambdaCreateArgs
)


class TestVpcSet(unittest.TestCase):

    LambdaArgsObject = LambdaCreateArgs()

    # test successes
    def test_vpc_set_success_no_input(self):
        self.LambdaArgsObject.vpc_set()
        self.assertEqual(self.LambdaArgsObject.vpc, LAMBDA_DEFAULT_VPC)

    def test_vpc_set_success_input(self):
        self.LambdaArgsObject.vpc_set(LAMBDA_DEFAULT_VPC)
        self.assertEqual(self.LambdaArgsObject.vpc, LAMBDA_DEFAULT_VPC)

    # test errors
    def test_vpc_set_error_input_not_in_allowed_versions(self):
        with self.assertRaises(ValueError):
            self.LambdaArgsObject.vpc_set(f'{LAMBDA_DEFAULT_VPC}-not-real-1234567890')


if __name__ == '__main__':
    unittest.main()
