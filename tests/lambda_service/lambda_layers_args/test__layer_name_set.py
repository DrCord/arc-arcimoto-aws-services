import unittest

from arcimoto_aws_services.lambda_service import LambdaLayersArgs


class Test_LayerNameSet(unittest.TestCase):

    LambdaArgsObject = LambdaLayersArgs()

    # test successes
    def test_layer_name_set_success(self):
        test_value = 'test name'
        self.LambdaArgsObject._layer_name_set(test_value)
        self.assertEqual(self.LambdaArgsObject.layer_name, test_value)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
