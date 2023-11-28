import unittest

from arcimoto_aws_services.aws_service import AwsService


class TestClientClose(unittest.TestCase):

    AwsServiceObject = None

    @classmethod
    def setUpClass(cls):
        cls.AwsServiceObject = AwsService()

    # test successes
    def test_client_close_success(self):
        self.AwsServiceObject.client_init()
        try:
            self.AwsServiceObject.client_close()
        except Exception as e:
            self.fail(f'client_close failed: {e}')
        # check client_local directly instead of client property to prevent re-opening connection
        self.assertIsNone(self.AwsServiceObject.client_local)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
