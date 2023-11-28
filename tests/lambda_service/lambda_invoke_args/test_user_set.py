import unittest

from arcimoto_aws_services.lambda_service import LambdaInvokeArgs


class TestUserSet(unittest.TestCase):

    LambdaArgsObject = LambdaInvokeArgs()

    # test successes
    def test_user_set_success(self):
        test_value = 'test123'
        self.LambdaArgsObject.user_set(test_value)
        self.assertEqual(self.LambdaArgsObject.user, test_value)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
