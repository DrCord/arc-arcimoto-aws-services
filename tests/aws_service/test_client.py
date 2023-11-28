import unittest

from arcimoto_aws_services.aws_service import AwsService


class TestClientInit(unittest.TestCase):

    AwsServiceObject = None

    @classmethod
    def setUpClass(cls):
        cls.AwsServiceObject = AwsService()

    # test successes
    def test_client_getter_success(self):
        self.assertEqual(
            str(type(self.AwsServiceObject.client)),
            "<class 'botocore.client.Lambda'>"
        )

    def test_client_setter_success(self):
        client_mock_data = 'client-1234567'
        self.AwsServiceObject.client = client_mock_data
        self.assertEqual(
            self.AwsServiceObject.client_local,
            client_mock_data
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
