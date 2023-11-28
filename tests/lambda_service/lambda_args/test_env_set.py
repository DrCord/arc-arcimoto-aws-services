import unittest

from arcimoto_aws_services.lambda_service import (
    DEV_ALIAS,
    LambdaArgs
)


class TestEnvSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_env_set_success(self):
        self.LambdaArgsObject.env_set()
        self.assertEqual(self.LambdaArgsObject.env, DEV_ALIAS)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
