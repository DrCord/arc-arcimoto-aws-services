import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs


class Test_ZipBytesSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_zip_bytes_set_success(self):
        test_value = 'not really a zip_bytes object! this could be improved'
        self.LambdaArgsObject._zip_bytes_set(test_value)
        self.assertEqual(self.LambdaArgsObject.zip_bytes, test_value)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
