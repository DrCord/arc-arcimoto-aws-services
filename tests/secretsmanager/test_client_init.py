import unittest

from arcimoto_aws_services.secretsmanager import SecretsManagerService


class TestClientInit(unittest.TestCase):

    SecretsManagerServiceObject = None

    @classmethod
    def setUpClass(cls):
        cls.SecretsManagerServiceObject = SecretsManagerService()

    # test successes
    def test_client_init_success(self):
        try:
            self.SecretsManagerServiceObject.client_init()
        except Exception as e:
            self.fail(f'client_init failed: {e}')
        self.assertEqual(
            str(type(self.SecretsManagerServiceObject.client)),
            "<class 'botocore.client.SecretsManager'>"
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
