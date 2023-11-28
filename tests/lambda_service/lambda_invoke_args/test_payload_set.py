import unittest

from arcimoto_aws_services.lambda_service import LambdaInvokeArgs


class TestPayloadSet(unittest.TestCase):

    LambdaArgsObject = LambdaInvokeArgs()

    # test successes
    def test_payload_set_success(self):
        test_payload = {'test_prop': 'test_value'}
        self.LambdaArgsObject.payload_set(test_payload)
        self.assertEqual(self.LambdaArgsObject.payload, test_payload)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
