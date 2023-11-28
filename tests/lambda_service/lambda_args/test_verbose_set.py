import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs


class TestDryRunSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_verbose_set_success_no_input(self):
        self.LambdaArgsObject.verbose_set()
        self.assertFalse(self.LambdaArgsObject.verbose)

    def test_verbose_set_success_input_false(self):
        self.LambdaArgsObject.verbose_set(False)
        self.assertFalse(self.LambdaArgsObject.verbose)

    def test_verbose_set_success_input_true(self):
        self.LambdaArgsObject.verbose_set(True)
        self.assertTrue(self.LambdaArgsObject.verbose)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
