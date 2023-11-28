import unittest

from arcimoto_aws_services.secretsmanager import SecretsManagerService

SECRET_NAME_TESTING = 'aws.cognito.unittest'


class TestGetSecret(unittest.TestCase):

    SecretsManagerServiceObject = None

    @classmethod
    def setUpClass(cls):
        cls.SecretsManagerServiceObject = SecretsManagerService()

    # test successes
    def test_get_secret_success(self):
        try:
            self.SecretsManagerServiceObject.get_secret(SECRET_NAME_TESTING)
        except Exception as e:
            self.fail(f'get_secret failed: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
