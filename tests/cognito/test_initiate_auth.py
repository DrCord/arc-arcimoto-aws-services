from botocore.exceptions import ParamValidationError
import unittest

from arcimoto_aws_services.cognito import CognitoAuthenticate

from .cognito import TestCognito


class TestInitiateAuth(unittest.TestCase):

    CognitoAuthenticateObject = None
    TestCognitoObject = None

    @classmethod
    def setUpClass(cls):
        cls.CognitoAuthenticateObject = CognitoAuthenticate()
        cls.TestCognitoObject = TestCognito()

    # test successes
    def test_initiate_auth_success(self):
        self.assertIsInstance(
            self.CognitoAuthenticateObject.initiate_auth(
                self.CognitoAuthenticateObject.client_id,
                self.TestCognitoObject.username,
                self.TestCognitoObject.password
            ),
            dict
        )

    # test errors
    def test_initiate_auth_error_client_id_null(self):
        with self.assertRaises(ParamValidationError):
            self.CognitoAuthenticateObject.initiate_auth(
                None,
                self.TestCognitoObject.username,
                self.TestCognitoObject.password
            )

    def test_initiate_auth_error_username_null(self):
        with self.assertRaises(ParamValidationError):
            self.CognitoAuthenticateObject.initiate_auth(
                self.CognitoAuthenticateObject.client_id,
                None,
                self.TestCognitoObject.password
            )

    def test_initiate_auth_error_password_null(self):
        with self.assertRaises(ParamValidationError):
            self.CognitoAuthenticateObject.initiate_auth(
                self.CognitoAuthenticateObject.client_id,
                self.TestCognitoObject.username,
                None
            )

    def test_initiate_auth_error_client_id_unknown(self):
        with self.assertRaises(self.CognitoAuthenticateObject.client.exceptions.ResourceNotFoundException):
            self.CognitoAuthenticateObject.initiate_auth(
                'unknownclientid1234567890',
                self.TestCognitoObject.username,
                self.TestCognitoObject.password
            )

    def test_initiate_auth_error_client_id_invalid_format(self):
        with self.assertRaises(self.CognitoAuthenticateObject.client.exceptions.InvalidParameterException):
            self.CognitoAuthenticateObject.initiate_auth(
                'invalid-format-client-id-1234567890',
                self.TestCognitoObject.username,
                self.TestCognitoObject.password
            )


if __name__ == '__main__':
    unittest.main()
