import unittest
import warnings

from arcimoto_aws_services.cognito import CognitoAuthenticate

from .cognito import TestCognito


class TestChallengeRespond(unittest.TestCase):

    CognitoAuthenticateObject = None
    TestCognitoObject = None

    challenge = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning,
            message='unclosed.*<ssl.SSLSocket.*>'
        )
        cls.CognitoAuthenticateObject = CognitoAuthenticate()
        cls.TestCognitoObject = TestCognito()

    # test successes
    # does not test success as requires an ongoing aws cognito authentication challenge
    # such as one of [NEW_PASSWORD_REQUIRED, SMS_MFA, SOFTWARE_TOKEN_MFA]

    # test errors
    def test_authenticate_error_non_interactive_username_null(self):
        with self.assertRaises(ValueError):
            self.CognitoAuthenticateObject.challenge_respond(
                'not-a-real-cognito-challenge-type'
            )


if __name__ == '__main__':
    unittest.main()
