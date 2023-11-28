import unittest

from arcimoto_aws_services.lambda_service import LambdaApiGatewayArgs
from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class TestApiArnSet(unittest.TestCase):

    LambdaApiGatewayArgsObject = LambdaApiGatewayArgs()

    # test successes
    def test_api_arn_set_success(self):
        self.LambdaApiGatewayArgsObject.api_arn_set(DEFAULT_TEST_LAMBDA_NAME)
        self.assertEqual(self.LambdaApiGatewayArgsObject.api_arn, DEFAULT_TEST_LAMBDA_NAME)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
