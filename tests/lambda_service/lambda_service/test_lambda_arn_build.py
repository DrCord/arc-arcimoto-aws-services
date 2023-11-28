import unittest

from arcimoto_aws_services.lambda_service import (
    LambdaArgs,
    LambdaService
)


class TestLambdaArnBuild(unittest.TestCase):

    args = None
    LambdaServiceObject = None

    @classmethod
    def setUpClass(cls):
        cls.args = LambdaArgs()

        cls.LambdaServiceObject = LambdaService(verbose=False)

    # test successes
    def test_lambda_arn_build_success(self):
        try:
            self.LambdaServiceObject.lambda_arn_build(
                self.args.region,
                self.args.account_id,
                self.args.function_name,
                'dev'
            )
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
