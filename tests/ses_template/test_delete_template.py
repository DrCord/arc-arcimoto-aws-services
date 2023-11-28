import unittest
from uuid import uuid4
import warnings

from arcimoto_aws_services.ses_template import SesTemplate


class TestDeleteTemplate(unittest.TestCase):

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
    def test_delete_template_success_template_does_not_exist(self):
        SesTemplateObject = SesTemplate(mute=True)
        SesTemplateObject.template = {'TemplateName': self.unit_test_template_name}
        try:
            SesTemplateObject.delete_template()
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertIsNone(SesTemplateObject.template)

    def test_delete_template_success_template_does_exist(self):
        SesTemplateObject = SesTemplate(mute=True)
        SesTemplateObject.create_template(**self.test_template)
        try:
            SesTemplateObject.delete_template()
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertIsNone(SesTemplateObject.template)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
