import unittest

from arcimoto_aws_services.lambda_service import LambdaCreateArgs


class TestDescriptionSet(unittest.TestCase):

    LambdaArgsObject = LambdaCreateArgs()

    # test successes
    def test_description_set_success(self):
        test_description = 'test description'
        self.LambdaArgsObject.description_set(test_description)
        self.assertEqual(self.LambdaArgsObject.description, test_description)


if __name__ == '__main__':
    unittest.main()
