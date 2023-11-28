import unittest

from arcimoto_aws_services.lambda_service import (
    LambdaArgs,
    LambdaApiGatewayService
)

from tests.constants import (
    DEFAULT_TEST_API_ID,
    DEFAULT_TEST_API_PATH
)


class TestApiArnBuild(unittest.TestCase):

    args = None
    LambdaServiceApiGatewayObject = None

    @classmethod
    def setUpClass(cls):
        cls.args = LambdaArgs()

        cls.LambdaServiceApiGatewayObject = LambdaApiGatewayService(
            verbose=False
        )

    # test successes
    def test_api_arn_build_success(self):
        try:
            self.LambdaServiceApiGatewayObject.api_arn_build(
                self.args.region,
                self.args.account_id,
                DEFAULT_TEST_API_ID,
                DEFAULT_TEST_API_PATH
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
