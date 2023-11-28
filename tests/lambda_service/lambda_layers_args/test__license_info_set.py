import unittest

from arcimoto_aws_services.lambda_service import (
    LICENSE_DEFAULT,
    LambdaLayersArgs
)


class Test_LicenseInfoSet(unittest.TestCase):

    LambdaArgsObject = LambdaLayersArgs()

    # test successes
    def test_license_info_set_success(self):
        self.LambdaArgsObject._license_info_set()
        self.assertEqual(self.LambdaArgsObject.license_info, LICENSE_DEFAULT)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
