import unittest

from arcimoto_aws_services.cognito import CognitoAuthenticate


class TestClientInit(unittest.TestCase):

    CognitoAuthenticateObject = None

    @classmethod
    def setUpClass(cls):
        cls.CognitoAuthenticateObject = CognitoAuthenticate()

    # test successes
    def test_client_init_success(self):
        try:
            self.CognitoAuthenticateObject.client_init()
        except Exception as e:
            self.fail(f'client_init failed: {e}')
        self.assertEqual(
            str(type(self.CognitoAuthenticateObject.client)),
            "<class 'botocore.client.CognitoIdentityProvider'>"
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
