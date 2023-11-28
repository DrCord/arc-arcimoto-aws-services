import unittest
import warnings

from arcimoto_aws_services.lambda_service import LambdaService


class TestClientInit(unittest.TestCase):

    LambdaServiceObject = None

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

        cls.LambdaServiceObject = LambdaService(verbose=False)

    # test successes
    def test_client_init_success(self):
        try:
            self.LambdaServiceObject.client_init()
        except Exception as e:
            self.fail(f'client_init failed: {e}')
        self.assertEqual(
            str(type(self.LambdaServiceObject.client)),
            "<class 'botocore.client.Lambda'>"
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
