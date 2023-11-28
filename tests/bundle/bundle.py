from tests.libraries import TestLibraries

from tests.constants import DEFAULT_TEST_LAMBDA_NAME


class TestBundle(TestLibraries):

    function_config = None
    function_name = DEFAULT_TEST_LAMBDA_NAME
    functions = None
    common_config = None
    global_dependencies = None

    def __init__(self):
        super().__init__()
