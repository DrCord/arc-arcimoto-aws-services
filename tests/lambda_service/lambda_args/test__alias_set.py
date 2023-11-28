import unittest

from arcimoto_aws_services.lambda_service import (
    DEV_ALIAS,
    LambdaArgs
)


class TestAliasSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test__alias_set_success(self):
        self.LambdaArgsObject._alias_set()
        self.assertEqual(self.LambdaArgsObject.alias, DEV_ALIAS)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
