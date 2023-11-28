import unittest

from arcimoto_aws_services.lambda_service import LambdaCreateArgs


class TestTagsSet(unittest.TestCase):

    LambdaArgsObject = LambdaCreateArgs()

    # test successes
    def test_tags_set_success(self):
        test_tags = {'unit-tests': ''}
        self.LambdaArgsObject.tags_set(test_tags)
        self.assertEqual(self.LambdaArgsObject.tags, test_tags)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
