import unittest

from arcimoto_aws_services.lambda_service import LambdaInvokeArgs
from arcimoto_aws_services.cognito import DEFAULT_CLIENT_ID


class TestClientIdSet(unittest.TestCase):

    LambdaArgsObject = LambdaInvokeArgs()

    # test successes
    def test_client_id_set_success(self):
        self.LambdaArgsObject.client_id_set()
        self.assertEqual(self.LambdaArgsObject.client_id, DEFAULT_CLIENT_ID)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
