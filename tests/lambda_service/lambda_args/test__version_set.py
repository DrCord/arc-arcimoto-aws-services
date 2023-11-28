import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs


class Test_VersionSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test__version_set_success(self):
        self.LambdaArgsObject._version_set()
        self.assertEqual(self.LambdaArgsObject.version, '$LATEST')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
