import unittest

from arcimoto_aws_services.ses_template import SesTemplate


class TestClientInit(unittest.TestCase):

    SesTemplateObject = None

    @classmethod
    def setUpClass(cls):
        cls.SesTemplateObject = SesTemplate()

    # test successes
    def test_client_init_success(self):
        try:
            self.SesTemplateObject.client_init()
        except Exception as e:
            self.fail(f'client_init failed: {e}')
        self.assertEqual(
            str(type(self.SesTemplateObject.client)),
            "<class 'botocore.client.SES'>"
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
