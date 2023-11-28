import unittest

from arcimoto_aws_services.lambda_service import LambdaLayersArgs


class Test_LayerDescriptionSet(unittest.TestCase):

    LambdaArgsObject = LambdaLayersArgs()

    # test successes
    def test_layer_description_set_success(self):
        test_value = 'test description'
        self.LambdaArgsObject._layer_description_set(test_value)
        self.assertEqual(self.LambdaArgsObject.layer_description, test_value)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
