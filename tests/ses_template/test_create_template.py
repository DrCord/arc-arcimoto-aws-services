import unittest
from uuid import uuid4
import warnings

from arcimoto_aws_services.ses_template import SesTemplate


class TestCreateTemplate(unittest.TestCase):

    SesTemplateObject = None
    unit_test_template_name = f'unit-test-{uuid4()}'
    test_template = {
        'name': unit_test_template_name,
        'subject': 'unit test email template',
        'text': "This is what {{name}} will {{action}} if {{name}} can't display HTML.",
        'html': "<p><i>This</i> is what {{name}} will {{action}} if {{name}} "
                "<b>can</b> display HTML.</p>"
    }

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_create_template_success(self):
        SesTemplateObject = SesTemplate(mute=True)
        try:
            SesTemplateObject.create_template(**self.test_template)
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertIsInstance(SesTemplateObject.template, dict)
        SesTemplateObject.delete_template()

    # test errors
    def test_create_template_error_template_already_exists(self):
        SesTemplateObject = SesTemplate(mute=True)
        SesTemplateObject.create_template(**self.test_template)
        with self.assertRaises(SesTemplateObject.client.exceptions.AlreadyExistsException):
            SesTemplateObject.create_template(**self.test_template)
        SesTemplateObject.delete_template()


if __name__ == '__main__':
    unittest.main()
