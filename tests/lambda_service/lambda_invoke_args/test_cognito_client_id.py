import unittest

from arcimoto_aws_services.lambda_service import LambdaInvokeArgs
from arcimoto_aws_services.cognito import DEFAULT_CLIENT_ID


class TestCognitoClientId(unittest.TestCase):

    LambdaArgsObject = LambdaInvokeArgs()

    # test successes
    def test_cognito_client_id_success(self):
        self.assertEqual(self.LambdaArgsObject.cognito_client_id, DEFAULT_CLIENT_ID)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
