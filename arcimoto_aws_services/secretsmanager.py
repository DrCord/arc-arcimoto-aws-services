import json

from arcimoto_aws_services.aws_service import AwsService


class SecretsManagerService(AwsService):

    client_local = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def client_init(self):
        return super().client_init('secretsmanager')

    def get_secret(self, secret_name):
        response = self.client.get_secret_value(
            SecretId=secret_name
        )
        return json.loads(response['SecretString'])
