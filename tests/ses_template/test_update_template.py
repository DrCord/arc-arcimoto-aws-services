from copy import deepcopy
import unittest
from uuid import uuid4
import warnings

from arcimoto_aws_services.ses_template import SesTemplate


class TestUpdateTemplate(unittest.TestCase):

    SesTemplateObject = None
    unit_test_template_name = None
    test_template = {
        'name': None,
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
        test_template = deepcopy(self.test_template)
        test_template['name'] = f'unit-test-{uuid4()}'
        SesTemplateObject.create_template(**test_template)
        try:
            SesTemplateObject.update_template(**test_template)
        except Exception as e:
            self.fail(f'test failed unexpectedly: {e}')
        self.assertIsInstance(SesTemplateObject.template, dict)
        SesTemplateObject.delete_template()

    # test errors
    def test_create_template_error_template_does_not_exist(self):
        SesTemplateObject = SesTemplate(mute=True)
        test_template = deepcopy(self.test_template)
        test_template['name'] = f'unit-test-{uuid4()}'
        with self.assertRaises(SesTemplateObject.client.exceptions.TemplateDoesNotExistException):
            SesTemplateObject.update_template(**test_template)


if __name__ == '__main__':
    unittest.main()
