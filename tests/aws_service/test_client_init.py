import unittest

from arcimoto_aws_services.aws_service import AwsService


class TestClientInit(unittest.TestCase):

    AwsServiceObject = None

    @classmethod
    def setUpClass(cls):
        cls.AwsServiceObject = AwsService()

    # test successes
    def test_client_init_success(self):
        try:
            self.AwsServiceObject.client_init()
        except Exception as e:
            self.fail(f'client_init failed: {e}')
        self.assertEqual(
            str(type(self.AwsServiceObject.client)),
            "<class 'botocore.client.Lambda'>"
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
