from tests.unit_tests_user_credentials import UnitTestsUserCredentials


class TestCognito():

    unit_test_user_credentials = None
    UnitTestsUserCredentialsObject = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UnitTestsUserCredentialsObject = UnitTestsUserCredentials()

    @property
    def password(self):
        return self.UnitTestsUserCredentialsObject.password

    @property
    def username(self):
        return self.UnitTestsUserCredentialsObject.username
