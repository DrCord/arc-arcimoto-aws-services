import unittest

from arcimoto_aws_services.lambda_service import LambdaArgs


class Test_DescriptionSet(unittest.TestCase):

    LambdaArgsObject = LambdaArgs()

    # test successes
    def test__description_set_success(self):
        self.LambdaArgsObject._description_set()
        self.assertIsNotNone(self.LambdaArgsObject.description)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
