# adapted from https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/ses/ses_templates.py#L10

import logging
from botocore.exceptions import ClientError

from arcimoto_aws_services.aws_service import AwsService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SesTemplate(AwsService):
    """Encapsulates Amazon SES template functions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = None
        self.mute = kwargs.get('mute', False)
        if self.mute:
            logger.setLevel(logging.ERROR)

    def client_init(self):
        return super().client_init('ses')

    @property
    def template_name(self):
        """
        :return: Gets the name of the template, if a template has been loaded.
        """
        return self.template['TemplateName'] if self.template is not None else None

    def create_template(self, name, subject, text, html):
        """
        Creates an email template.

        :param name: The name of the template.
        :param subject: The subject of the email.
        :param text: The plain text version of the email.
        :param html: The HTML version of the email.
        """
        try:
            template = {
                'TemplateName': name,
                'SubjectPart': subject,
                'TextPart': text,
                'HtmlPart': html
            }
            self.client.create_template(Template=template)
            logger.info(f'Created template {name}')
            self.template = template
        except ClientError:
            logger.warning(f'Unable to create template {name}.')
            raise

    def delete_template(self):
        """
        Deletes an email template.
        """
        try:
            self.client.delete_template(TemplateName=self.template_name)
            logger.info(f'Deleted template {self.template_name}')
            self.template = None
        except ClientError:
            logger.warning(f'Unable to delete template {self.template_name}')
            raise

    def get_template(self, name):
        """
        Gets a previously created email template.

        :param name: The name of the template to retrieve.
        :return: The retrieved email template.
        """
        try:
            response = self.client.get_template(TemplateName=name)
            self.template = response['Template']
            logger.info(f'Retrieved template {name}')
        except ClientError as e:
            if e.response['Error']['Code'] == 'TemplateDoesNotExist':
                logger.info(f'Unable to get template {name}, it does not exist.')
                self.template = None
                return False
            else:
                logger.warning(f'Unable to get template {name}')
                raise
        else:
            return self.template

    def list_templates(self):
        """
        Gets a list of all email templates for the current account.

        :return: The list of retrieved email templates.
        """
        try:
            response = self.client.list_templates()
            templates = response['TemplatesMetadata']
            logger.info(f'Retrieved {len(templates)} templates')
        except ClientError:
            logger.warning('Unable to list templates')
            raise
        else:
            return templates

    def update_template(self, name, subject, text, html):
        """
        Updates a previously created email template.

        :param name: The name of the template.
        :param subject: The subject of the email.
        :param text: The plain text version of the email.
        :param html: The HTML version of the email.
        """
        try:
            template = {
                'TemplateName': name,
                'SubjectPart': subject,
                'TextPart': text,
                'HtmlPart': html
            }
            self.client.update_template(Template=template)
            logger.info(f'Updated template {name}')
            self.template = template
        except ClientError:
            logger.warning(f'Unable to update template {name}')
            raise
