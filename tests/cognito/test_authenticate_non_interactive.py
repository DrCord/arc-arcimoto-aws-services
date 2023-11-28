from botocore.exceptions import ParamValidationError
import unittest
import warnings

from arcimoto_aws_services.cognito import CognitoAuthenticate

from .cognito import TestCognito


class TestAuthenticateNonInteractive(unittest.TestCase):

    CognitoAuthenticateObject = None
    TestCognitoObject = None

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
    def test_authenticate_non_interactive_success(self):
        self.assertIsInstance(
            self.CognitoAuthenticateObject.authenticate_non_interactive(
                self.TestCognitoObject.username,
                self.TestCognitoObject.password
            ),
            str
        )

    # test errors
    def test_authenticate_non_interactive_error_username_null(self):
        with self.assertRaises(ParamValidationError):
            self.CognitoAuthenticateObject.authenticate_non_interactive(
                None,
                self.TestCognitoObject.password
            )

    def test_authenticate_non_interactive_error_password_null(self):
        with self.assertRaises(ParamValidationError):
            self.CognitoAuthenticateObject.authenticate_non_interactive(
                self.TestCognitoObject.username,
                None
            )

    def test_authenticate_non_interactive_error_client_id_unknown(self):
        CognitoAuthenticateObject = CognitoAuthenticate('notarealclientid')
        with self.assertRaises(self.CognitoAuthenticateObject.client.exceptions.ResourceNotFoundException):
            CognitoAuthenticateObject.authenticate_non_interactive(
                self.TestCognitoObject.username,
                self.TestCognitoObject.password
            )

    def test_authenticate_non_interactive_error_client_id_invalid_format(self):
        CognitoAuthenticateObject = CognitoAuthenticate('not-a-real-client-id')
        with self.assertRaises(self.CognitoAuthenticateObject.client.exceptions.InvalidParameterException):
            CognitoAuthenticateObject.authenticate_non_interactive(
                self.TestCognitoObject.username,
                self.TestCognitoObject.password
            )


if __name__ == '__main__':
    unittest.main()
