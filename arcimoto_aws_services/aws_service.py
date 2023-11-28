import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

DEFAULT_AWS_ACCOUNT_ID = '511596272857'
DEFAULT_AWS_REGION = 'us-west-2'


class AwsService:
    global logger, DEFAULT_AWS_ACCOUNT_ID, DEFAULT_AWS_REGION

    account_id = None
    client_local = None
    region = DEFAULT_AWS_REGION

    def __init__(self, account_id=DEFAULT_AWS_ACCOUNT_ID, region=DEFAULT_AWS_REGION, *args, **kwargs):
        self.account_id = account_id
        self.region = region

    @property
    def client(self):
        if self.client_local is None:
            self.client_init()
        return self.client_local

    @client.setter
    def client(self, value):
        self.client_local = value

    def client_close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def client_init(self, service='lambda'):
        self.client = boto3.client(service, self.region)
