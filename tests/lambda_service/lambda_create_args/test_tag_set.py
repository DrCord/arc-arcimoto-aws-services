import unittest

from arcimoto_aws_services.lambda_service import LambdaCreateArgs


class TestTagSet(unittest.TestCase):

    LambdaArgsObject = LambdaCreateArgs()

    # test successes
    def test_tag_set_success(self):
        test_tag = ['unit-test']
        self.LambdaArgsObject.tag_set(test_tag)
        self.assertEqual(self.LambdaArgsObject.tag, test_tag)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
