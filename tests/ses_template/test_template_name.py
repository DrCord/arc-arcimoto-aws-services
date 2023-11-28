import unittest

from arcimoto_aws_services.ses_template import SesTemplate


class TestTemplateName(unittest.TestCase):

    SesTemplateObject = None
    template_name = 'unit-test'

    @classmethod
    def setUpClass(cls):
        cls.SesTemplateObject = SesTemplate()

    # test successes
    def test_template_name_success(self):
        self.assertIsNone(self.SesTemplateObject.template_name)
        self.SesTemplateObject.template = {'TemplateName': self.template_name}
        self.assertEqual(
            self.SesTemplateObject.template_name,
            self.template_name
        )

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
