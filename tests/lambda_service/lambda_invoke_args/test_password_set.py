import unittest

from arcimoto_aws_services.lambda_service import LambdaInvokeArgs


class TestPasswordSet(unittest.TestCase):

    LambdaArgsObject = LambdaInvokeArgs()

    # test successes
    def test_password_set_success(self):
        test_value = 'test123'
        self.LambdaArgsObject.password_set(test_value)
        self.assertEqual(self.LambdaArgsObject.password, test_value)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
