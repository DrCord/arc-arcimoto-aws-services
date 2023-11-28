import unittest
from uuid import uuid4
import warnings

from arcimoto_aws_services.ses_template import SesTemplate


class TestListTemplates(unittest.TestCase):

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
    def test_list_templates_success(self):
        response = None
        SesTemplateObject = SesTemplate(mute=True)
        try:
            response = SesTemplateObject.list_templates()
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertTrue(response)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
