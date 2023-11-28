import unittest
from uuid import uuid4
import warnings

from arcimoto_aws_services.ses_template import SesTemplate


class TestGetTemplate(unittest.TestCase):

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
    def test_get_template_success_template_does_not_exist(self):
        response = None
        SesTemplateObject = SesTemplate(mute=True)
        try:
            SesTemplateObject.get_template(f'unit-test-{uuid4()}')
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertFalse(response)

    def test_get_template_success_template_does_exist(self):
        response = None
        SesTemplateObject = SesTemplate(mute=True)
        SesTemplateObject.create_template(**self.test_template)
        try:
            response = SesTemplateObject.get_template(self.unit_test_template_name)
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertIsInstance(response, dict)
        SesTemplateObject.delete_template()

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
