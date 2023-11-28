import unittest

from arcimoto_aws_services.lambda_service import (
    DEFAULT_AWS_ACCOUNT_ID,
    LambdaArgs
)


class TestAccountIdSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_account_id_set_success_no_input(self):
        self.LambdaArgsObject.account_id_set()
        self.assertEqual(self.LambdaArgsObject.account_id, DEFAULT_AWS_ACCOUNT_ID)

    def test_account_id_set_success_input(self):
        fake_account_id = 'test-account-id-value-1234567890'
        self.LambdaArgsObject.account_id_set(fake_account_id)
        self.assertEqual(self.LambdaArgsObject.account_id, fake_account_id)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
