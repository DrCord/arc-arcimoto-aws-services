import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs


class TestMuteSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_mute_set_success_no_input(self):
        self.LambdaArgsObject.mute_set()
        self.assertFalse(self.LambdaArgsObject.mute)

    def test_mute_set_success_input_false(self):
        self.LambdaArgsObject.mute_set(False)
        self.assertFalse(self.LambdaArgsObject.mute)

    def test_mute_set_success_input_true(self):
        self.LambdaArgsObject.mute_set(True)
        self.assertTrue(self.LambdaArgsObject.mute)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
