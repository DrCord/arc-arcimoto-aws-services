import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs


class TestDryRunSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test_dry_run_set_success_no_input(self):
        self.LambdaArgsObject.dry_run_set()
        self.assertFalse(self.LambdaArgsObject.dry_run)

    def test_dry_run_set_success_input_false(self):
        self.LambdaArgsObject.dry_run_set(False)
        self.assertFalse(self.LambdaArgsObject.dry_run)

    def test_dry_run_set_success_input_true(self):
        self.LambdaArgsObject.dry_run_set(True)
        self.assertTrue(self.LambdaArgsObject.dry_run)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
