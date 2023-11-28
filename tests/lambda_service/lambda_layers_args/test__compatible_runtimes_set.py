import unittest

from arcimoto_aws_services.lambda_service import (
    LAMBDA_LAYERS_COMPATIBLE_RUNTIMES,
    LambdaLayersArgs
)


class Test_CompatibleRuntimesSet(unittest.TestCase):

    LambdaArgsObject = LambdaLayersArgs()

    # test successes
    def test_compatible_runtimes_set_success(self):
        self.LambdaArgsObject._compatible_runtimes_set()
        self.assertEqual(self.LambdaArgsObject.compatible_runtimes, LAMBDA_LAYERS_COMPATIBLE_RUNTIMES)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
