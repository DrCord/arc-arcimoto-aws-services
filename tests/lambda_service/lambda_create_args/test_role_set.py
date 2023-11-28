import unittest

from arcimoto_aws_services.lambda_service import LambdaCreateArgs
from tests.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME


class TestRoleSet(unittest.TestCase):

    LambdaArgsObject = LambdaCreateArgs()

    # test successes
    def test_role_set_success(self):
        self.LambdaArgsObject.role_set(DEFAULT_TEST_LAMBDA_ROLE_NAME)
        self.assertEqual(self.LambdaArgsObject.role, DEFAULT_TEST_LAMBDA_ROLE_NAME)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
