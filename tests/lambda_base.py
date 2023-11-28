import uuid

from tests.constants import (
    DEFAULT_TEST_LAMBDA_NAME,
    DEFAULT_TEST_LAMBDA_ROLE_NAME
)


class LambdaBase:

    _lambda_name = None
    _role = DEFAULT_TEST_LAMBDA_ROLE_NAME

    def __init__(self, lambda_name=DEFAULT_TEST_LAMBDA_NAME, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lambda_name = lambda_name

    @property
    def lambda_name(self):
        if self._lambda_name is None:
            self._lambda_name_set()
        return self._lambda_name

    @lambda_name.setter
    def lambda_name(self, value):
        self._lambda_name_set(value)

    # @property function - for convenience/backwards compatibility
    @property
    def function(self):
        return self.lambda_name

    @lambda_name.setter
    def function(self, value):  # noqa: F811
        self.lambda_name = value

    # @property function_name - for convenience/backwards compatibility
    @property
    def function_name(self):
        return self.lambda_name

    @lambda_name.setter
    def function_name(self, value):  # noqa: F811
        self.lambda_name = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    def _lambda_name_set(self, lambda_name=DEFAULT_TEST_LAMBDA_NAME):
        self._lambda_name = lambda_name
        if lambda_name == DEFAULT_TEST_LAMBDA_NAME:
            self._lambda_name += f'_{str(uuid.uuid4())}'
