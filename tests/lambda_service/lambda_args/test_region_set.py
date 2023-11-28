import unittest

from arcimoto_aws_services.lambda_service import (
    DEFAULT_AWS_REGION,
    LambdaArgs
)


class TestRegionSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_region_set_success_no_input(self):
        self.LambdaArgsObject.region_set()
        self.assertEqual(self.LambdaArgsObject.region, DEFAULT_AWS_REGION)

    def test_region_set_success_input(self):
        fake_region = 'test-region-value-1234567890'
        self.LambdaArgsObject.region_set(fake_region)
        self.assertEqual(self.LambdaArgsObject.region, fake_region)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
