import unittest

from arcimoto_aws_services.aws_service import (
    AwsService,
    DEFAULT_AWS_ACCOUNT_ID,
    DEFAULT_AWS_REGION
)


class TestInit(unittest.TestCase):

    AwsServiceObject = None

    # test successes
    def test_init_success_no_input(self):
        self.AwsServiceObject = AwsService()
        self.assertEqual(
            self.AwsServiceObject.account_id,
            DEFAULT_AWS_ACCOUNT_ID
        )
        self.assertEqual(
            self.AwsServiceObject.region,
            DEFAULT_AWS_REGION
        )

    def test_init_success_input(self):
        self.AwsServiceObject = AwsService(DEFAULT_AWS_ACCOUNT_ID, DEFAULT_AWS_REGION)
        self.assertEqual(
            self.AwsServiceObject.account_id,
            DEFAULT_AWS_ACCOUNT_ID
        )
        self.assertEqual(
            self.AwsServiceObject.region,
            DEFAULT_AWS_REGION
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
