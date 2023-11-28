from botocore.exceptions import (
    ClientError,
    ParamValidationError
)
import json
import logging
import tempfile
import time
import uuid

from arcimoto_aws_services import (
    bundle,
    path
)

from arcimoto_aws_services.cognito import DEFAULT_CLIENT_ID
from arcimoto_aws_services.aws_service import (
    AwsService,
    DEFAULT_AWS_ACCOUNT_ID,
    DEFAULT_AWS_REGION
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

ALIASES = ['dev', 'staging', 'prod']

DEV_ALIAS = 'dev'
STAGING_ALIAS = 'staging'
PROD_ALIAS = 'prod'

PYTHON3_ALLOWED_MINOR_VERSIONS = [8]
PYTHON3_MINOR_VERSION_DEFAULT = 8

LAMBDA_DEFAULT_TIMEOUT = 30

# with 5 seconds between retries this equates to approximately 2 minutes
AWS_ACTION_RETRY_ATTEMPTS_DEFAULT = 24

LAMBDA_DEFAULT_VPC = 'main'
LAMBDA_ALLOWED_VPCS = [
    'none',
    'authkey',
    'main',
    'reef',
    'telemetry',
    'users',
    'yrisk'
]

LAMBDA_LAYERS_COMPATIBLE_RUNTIMES = ['python3.8']
LICENSE_DEFAULT = 'private: owned by Arcimoto, Inc.'

GLOBAL_DEPENDENCIES_LAYER_IDENTIFIERS = [
    'global_dependencies',
    'global_dependencies_dev',
    'global_dependencies_staging',
    'global_dependencies_test'
]

LAYER_ARN_BASE = 'arn:aws:lambda:us-west-2:511596272857:layer:'


class LambdaService(AwsService):
    global logger

    HANDLER_TEMPLATE = 'lambda/{}.lambda_handler'
    LAMBDA_ARN_TEMPLATE = 'arn:aws:lambda:{}:{}:function:{}:{}'
    ROLE_ARN_TEMPLATE = 'arn:aws:iam::{}:role/{}'
    VPC_CONFIG = {
        'none': {
            'SubnetIds': [],
            'SecurityGroupIds': []
        },
        'authkey': {
            'SubnetIds': [
                'subnet-005ff3d1d84186bf4',
                'subnet-0afde9781535df8e7',
                'subnet-0dd61b2a75481f5ca'
            ],
            'SecurityGroupIds': [
                'sg-0780fed677312643f'
            ]
        },
        'main': {
            'SubnetIds': [
                'subnet-0bea9313b52912a56',
                'subnet-007270db40c908dda',
                'subnet-0e56cc9c810c5953b'
            ],
            'SecurityGroupIds': [
                'sg-076496b494f53f884'
            ]
        },
        'reef': {
            'SubnetIds': [
                'subnet-064b1e83c9c61a874',
                'subnet-058c8df1a7144d7b4',
                'subnet-0068c9558f232e3e4'
            ],
            'SecurityGroupIds': [
                'sg-092b3da37946e1e4c'
            ]
        },
        'telemetry': {
            'SubnetIds': [
                'subnet-0ec9537da93eb41aa',
                'subnet-00aba450b1fc2f51c',
                'subnet-020ea71360cb27307'
            ],
            'SecurityGroupIds': [
                'sg-08f4bceaa69bb9dc4'
            ]
        },
        'users': {
            'SubnetIds': [
                'subnet-06c37e792b4f66dc6',
                'subnet-0a3d56887187f688c',
                'subnet-04f4c43d8a0e52518'
            ],
            'SecurityGroupIds': [
                'sg-0f666ac9d0d998d9c'
            ]
        },
        'yrisk': {
            'SubnetIds': [
                'subnet-02acd20d4a856c1d8',
                'subnet-07f27a469e781798c',
                'subnet-06c9aed37d5276c6b'
            ],
            'SecurityGroupIds': [
                'sg-0ccc5aea87298020f'
            ]
        }
    }

    client_local = None
    layers = {}
    verbose = None
    zip_bytes = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.verbose = kwargs.get('verbose', True)

        if self.verbose:
            logger.setLevel(logging.DEBUG)

    def add_layers(self, **kwargs):
        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.verbose, bool):
            raise ValueError(f'Invalid input verbose `{LambdaArgsObject.verbose}`, must be a Boolean.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        self._layers_add_to_lambda(
            LambdaArgsObject.function_name,
            LambdaArgsObject.verbose,
            LambdaArgsObject.mute
        )
        self.client_close()

    def archive_create(self, **kwargs):
        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        if not LambdaArgsObject.mute:
            logger.info('Creating archive...')

        zip_path = bundle.create_function_bundle(LambdaArgsObject.function_name)
        with open(zip_path, 'rb') as f:
            self.zip_bytes = f.read()

        return self.zip_bytes

    def client_init(self):
        return super().client_init('lambda')

    def create(self, **kwargs):
        LambdaArgsObject = LambdaCreateArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.description, str):
            raise ValueError(f'Invalid input description `{LambdaArgsObject.description}`, must be a string.')

        if LambdaArgsObject.zip_bytes is None:
            raise ValueError(f'Invalid input zip_bytes `{LambdaArgsObject.zip_bytes}`.')

        if LambdaArgsObject.role is None:
            raise ValueError(f'Invalid input role `{LambdaArgsObject.role}`.')

        if LambdaArgsObject.vpc not in self.VPC_CONFIG.keys():
            raise ValueError(f"Invalid input vpc `{LambdaArgsObject.vpc}`, must be one of: {', '.join(self.VPC_CONFIG.keys())}.")

        if LambdaArgsObject.timeout is None or LambdaArgsObject.timeout < 1:
            raise ValueError(f'Invalid input timeout `{LambdaArgsObject.timeout}`, must be a positive integer.')

        if LambdaArgsObject.python3_minor_version is None:
            raise ValueError(f'Invalid input python3_minor_version `{LambdaArgsObject.python3_minor_version}`.')

        if LambdaArgsObject.tags is None or not isinstance(LambdaArgsObject.tags, dict):
            raise ValueError(f'Invalid input tags `{LambdaArgsObject.tags}`, must be a dictionary.')

        if not isinstance(LambdaArgsObject.verbose, bool):
            raise ValueError(f'Invalid input verbose `{LambdaArgsObject.verbose}`, must be a Boolean.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        try:
            lambda_vpc_config = self.VPC_CONFIG[LambdaArgsObject.vpc]
        except Exception as e:
            raise ValueError(f"Invalid vpc '{LambdaArgsObject.vpc}' provided: {e}")

        # create lambda via AWS API
        if not LambdaArgsObject.mute:
            logger.info(f"Creating lambda '{LambdaArgsObject.function_name}'...")

        try:
            response = self.client.create_function(
                FunctionName=LambdaArgsObject.function_name,
                Runtime=f'python3.{LambdaArgsObject.python3_minor_version}',
                Role=self.ROLE_ARN_TEMPLATE.format(self.account_id, LambdaArgsObject.role),
                Handler=self.HANDLER_TEMPLATE.format(LambdaArgsObject.function_name),
                Code={'ZipFile': LambdaArgsObject.zip_bytes},
                Description=LambdaArgsObject.description,
                Timeout=LambdaArgsObject.timeout,
                Publish=False,
                VpcConfig=lambda_vpc_config,
                Tags=LambdaArgsObject.tags
            )
            if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                logger.info(f'Create lambda response:\n\n{json.dumps(response)}\n')
        except ClientError as e:
            if not LambdaArgsObject.mute:
                if e.response['Error']['Code'] == 'ResourceConflictException':
                    logger.warning(f'create_function resource conflict exception: {e}')
                else:
                    logger.warning(f'create_function client error: {e}')
            return None
        except Exception as e:
            if not LambdaArgsObject.mute:
                logger.warning(f'create_function exception: {e}')
            return None

        arn = response.get('FunctionArn', None)
        if not LambdaArgsObject.mute:
            logger.info(f'Created lambda with ARN {arn}')

        self.client_close()

        return arn

    def _create_function_layers_list(self, function_name):
        (functions_config, common_config, global_config) = bundle.load_dependencies()
        function_config = functions_config.get(function_name, None)
        if function_config is None:
            raise KeyError(f'No configuration found for function {function_name}')

        layers = self._layers_for_function(function_name, function_config, common_config)

        # lambdas cannot have more than 5 layers
        if len(layers) > 5:
            raise Exception(f'Lambda {function_name} cannot have more than 5 layers')

        return layers

    def delete(self, **kwargs):
        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.verbose, bool):
            raise ValueError(f'Invalid input verbose `{LambdaArgsObject.verbose}`, must be a Boolean.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        if not LambdaArgsObject.mute:
            logger.info(f"Deleting lambda '{LambdaArgsObject.function_name}'...")
        try:
            response = self.client.delete_function(
                FunctionName=LambdaArgsObject.function_name
            )
            if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                logger.info(f'delete_function response:\n\n{json.dumps(response)}\n')
        except Exception as e:
            if not LambdaArgsObject.mute:
                logger.warning(f'delete_function {LambdaArgsObject.function_name} failed: {e}')
            return False
        finally:
            self.client_close()

        return True

    def get_latest_global_dependencies_layer(self, env='prod', verbose=False, mute=False):
        if env not in ALIASES:
            raise ValueError(f'Input env must be one of: {ALIASES}')
        layer_name = 'arcimoto-globals'
        if env in ['dev', 'staging']:
            layer_name += f'-{env}'
        return self.get_latest_layer(layer_name, verbose, mute)

    def get_latest_global_dependencies_layer_version(self, env='prod', verbose=False, mute=False):
        if env not in ALIASES:
            raise ValueError(f'Input env must be one of: {ALIASES}')
        return self.get_latest_global_dependencies_layer(env, verbose, mute).get('Version')

    def get_latest_layer(self, layer_name='arcimoto-globals', verbose=False, mute=False):
        if layer_name not in self.layers.keys():
            self.list_layer_versions(layer_name, verbose, mute)
        if layer_name not in self.layers.keys():
            raise ValueError(f'Input layer_name {layer_name} not found in layers')
        max_version_layer = max(self.layers[layer_name], key=lambda x: x['Version'])
        return max_version_layer

    def invoke(self, **kwargs):
        LambdaArgsObject = LambdaInvokeArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.env, str):
            raise ValueError(f'Invalid input env `{LambdaArgsObject.env}`, must be a string.')

        if LambdaArgsObject.env not in ALIASES:
            raise ValueError(f'Invalid input env `{LambdaArgsObject.env}`, must be on of: {", ".join(ALIASES)}')

        if not isinstance(LambdaArgsObject.payload, dict):
            raise ValueError(f'Invalid input payload `{LambdaArgsObject.payload}`, must be a Dictionary.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        try:
            call_result = self.client.invoke(
                FunctionName=f'{LambdaArgsObject.function_name}:{LambdaArgsObject.env}',
                InvocationType='RequestResponse',
                Payload=json.dumps(LambdaArgsObject.payload)
            )
            # until read the streaming body from the invoke repsonse cannot be used readily
            response = json.loads(call_result['Payload'].read())
            if 'FunctionError' in call_result:
                exception_data = {
                    'error_type': response.get('errorType', None),
                    'error_message': str(response['errorMessage'])
                }
                raise Exception(json.dumps(exception_data))
            if not LambdaArgsObject.mute:
                logger.info(f'Response:\n\n{json.dumps(response, indent=2)}\n')
            return response
        except Exception as e:
            if not LambdaArgsObject.mute:
                logger.error(f'Execution error: {e}')
            raise e

    def lambda_alias_create(self, **kwargs):
        global ALIASES

        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if LambdaArgsObject.alias not in ALIASES:
            raise ValueError(f'Invalid input alias `{LambdaArgsObject.alias}`, must be one of: {", ".join(ALIASES)}')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        if not LambdaArgsObject.mute:
            logger.info(f'Creating `{LambdaArgsObject.alias}` alias for lambda `{LambdaArgsObject.function_name}`...')

        # force dev env to LATEST version, ignore input
        if LambdaArgsObject.alias == DEV_ALIAS:
            LambdaArgsObject._version_set()
        # for staging/prod require and use input version
        else:
            if LambdaArgsObject.version is None:
                raise ValueError('Input `version` required for any non-`dev` env.')
            LambdaArgsObject._version_set(LambdaArgsObject.version)

        try:
            response = self.client.create_alias(
                FunctionName=LambdaArgsObject.function_name,
                Name=LambdaArgsObject.alias,
                FunctionVersion=LambdaArgsObject.version,
                Description=f'{LambdaArgsObject.alias} environment'
            )
            if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                logger.info(f"Add '{LambdaArgsObject.alias}' alias to lambda response:\n\n{json.dumps(response)}\n")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                if not LambdaArgsObject.mute:
                    logger.info(f'Lambda `{LambdaArgsObject.function_name}` not found: {e}')
                raise e
            elif e.response['Error']['Code'] == 'ResourceConflictException':
                if not LambdaArgsObject.mute:
                    logger.info(f'Lambda `{LambdaArgsObject.function_name}` alias `{LambdaArgsObject.alias}` already exists: {e}')
                raise e
            else:
                if not LambdaArgsObject.mute:
                    logger.info(f'Lambda `{LambdaArgsObject.function_name}` create_alias failed with ClientError: {e}')
                raise e
        except Exception as e:
            raise Exception(f'create_alias exception: {e}')

        if not LambdaArgsObject.mute:
            logger.info(f'Added alias `{LambdaArgsObject.alias}` to lambda `{LambdaArgsObject.function_name}`')

        return True

    def lambda_alias_exists(self, **kwargs):
        return bool(self.lambda_alias_latest_version_get(
            function_name=kwargs.get('function_name'),
            alias=kwargs.get('alias'),
            mute=kwargs.get('mute', False)
        ))

    def lambda_alias_latest_version_get(self, **kwargs):
        global ALIASES

        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if LambdaArgsObject.alias not in ALIASES:
            raise ValueError(f'Invalid input alias `{LambdaArgsObject.alias}`, must be one of: {", ".join(ALIASES)}')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        try:
            get_alias_response = self.client.get_alias(
                FunctionName=LambdaArgsObject.function_name,
                Name=LambdaArgsObject.alias
            )
            if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                logger.info(f'Response from get_alias for `{LambdaArgsObject.function_name}:{LambdaArgsObject.alias}` - {get_alias_response}')
            version = get_alias_response.get('FunctionVersion', None)
            if version is None:
                if not LambdaArgsObject.mute:
                    logger.error(f'Unable to lookup alias `{LambdaArgsObject.alias}` for `{LambdaArgsObject.function_name}`')
                return False
            return version
        except self.client.exceptions.ResourceNotFoundException:
            return False

    def lambda_alias_update(self, **kwargs):
        global ALIASES

        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if LambdaArgsObject.alias not in ALIASES:
            raise ValueError(f'Invalid input alias `{LambdaArgsObject.alias}`, must be one of: {", ".join(ALIASES)}')

        if not isinstance(LambdaArgsObject.version, str):
            raise ValueError(f'Invalid input version `{LambdaArgsObject.version}`, must be an string.')

        if not isinstance(LambdaArgsObject.description, str):
            raise ValueError(f'Invalid input description `{LambdaArgsObject.description}`, must be a string.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        try:
            response = self.client.update_alias(
                FunctionName=LambdaArgsObject.function_name,
                Name=LambdaArgsObject.alias,
                FunctionVersion=LambdaArgsObject.version,
                Description=LambdaArgsObject.description
            )
            if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                logger.info(f'update_alias response: {response}')
            return response
        except Exception as e:
            if not LambdaArgsObject.mute:
                logger.error(f'update_alias fail: {e}')
            raise e

    def lambda_alias_upsert(self, **kwargs):
        global ALIASES

        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        if not self.lambda_alias_exists(
            function_name=LambdaArgsObject.function_name,
            alias=LambdaArgsObject.alias,
            mute=LambdaArgsObject.mute,
            verbose=LambdaArgsObject.verbose
        ):
            return self.lambda_alias_create(
                function_name=LambdaArgsObject.function_name,
                alias=LambdaArgsObject.alias,
                version=LambdaArgsObject.version,
                mute=LambdaArgsObject.mute,
                verbose=LambdaArgsObject.verbose
            )
        else:
            return self.lambda_alias_update(
                function_name=LambdaArgsObject.function_name,
                alias=LambdaArgsObject.alias,
                version=LambdaArgsObject.version,
                description=LambdaArgsObject.description,
                mute=LambdaArgsObject.mute,
                verbose=LambdaArgsObject.verbose
            )

    def lambda_arn_build(self, region, account_id, lambda_name, env):
        return self.LAMBDA_ARN_TEMPLATE.format(region, account_id, lambda_name, env)

    def lambda_dev_alias_create(self, **kwargs):
        global DEV_ALIAS

        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.verbose, bool):
            raise ValueError(f'Invalid input verbose `{LambdaArgsObject.verbose}`, must be a Boolean.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        self.lambda_alias_create(
            function_name=LambdaArgsObject.function_name,
            alias=DEV_ALIAS,
            verbose=LambdaArgsObject.verbose,
            mute=LambdaArgsObject.mute
        )

    def lambda_exists(self, **kwargs):
        try:
            self.invoke(
                function_name=kwargs.get('function_name', None),
                env=kwargs.get('alias', DEV_ALIAS),
                payload=kwargs.get('payload', {}),
                mute=kwargs.get('mute', False)
            )
            return True
        except self.client.exceptions.ResourceNotFoundException:
            return False

    def lambda_publish_version(self, **kwargs):
        LambdaArgsObject = LambdaArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.verbose, bool):
            raise ValueError(f'Invalid input verbose `{LambdaArgsObject.verbose}`, must be a Boolean.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        version_published = False
        count = 0
        # if lambda is in pending state update_function_configuration fails
        while not version_published and count < LambdaArgsObject.retry_attempts:
            count += 1
            time.sleep(5)
            try:
                publish_version_response = self.client.publish_version(
                    FunctionName=LambdaArgsObject.function_name
                )
                if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                    logger.info(f'publish_version response: {publish_version_response}')
            except ClientError as e:
                response_error_code = e.response['Error']['Code']
                if response_error_code == 'ResourceConflictException':
                    if not LambdaArgsObject.mute:
                        logger.info(f'Lambda {LambdaArgsObject.function_name} in pending state, waiting and retrying publish version')
                    continue
                elif response_error_code == 'TooManyRequestsException':
                    if not LambdaArgsObject.mute:
                        logger.info(f'Too many requests, waiting and retrying publish version for {LambdaArgsObject.function_name}')
                    continue
                elif response_error_code == 'ResourceNotFoundException':
                    if not LambdaArgsObject.mute:
                        logger.error(f'Failed to publish version - ResourceNotFoundException: {LambdaArgsObject.region}:{LambdaArgsObject.function_name}')
                    return False
                else:
                    if not LambdaArgsObject.mute:
                        logger.error(f'Failed to publish version - ClientError: {response_error_code}: {e}')
                    return False
            except Exception as e:
                if not LambdaArgsObject.mute:
                    logger.error(f'Failed to publish version: {e}')
                return False

            if not LambdaArgsObject.mute:
                logger.info(f'Lambda {LambdaArgsObject.function_name} version published')
            version_published = True

        version = publish_version_response.get('Version', None)
        if version is None:
            if not LambdaArgsObject.mute:
                logger.error(f'Failed to create version of {LambdaArgsObject.function_name}')
            return False

        return version

    def lambda_runtime_set(self, **kwargs):
        LambdaArgsObject = LambdaRuntimeArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if int(LambdaArgsObject.python3_minor_version) not in PYTHON3_ALLOWED_MINOR_VERSIONS:
            raise ValueError(f'Invalid input python3_minor_version `{LambdaArgsObject.python3_minor_version}`, must be one of: {"".join(PYTHON3_ALLOWED_MINOR_VERSIONS)}')

        if not isinstance(LambdaArgsObject.verbose, bool):
            raise ValueError(f'Invalid input verbose `{LambdaArgsObject.verbose}`, must be a Boolean.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        if not LambdaArgsObject.mute:
            logger.info(f'Preparing to update {LambdaArgsObject.function_name} runtime...')

        runtime_set = False
        count = 0
        # if lambda is in pending state update_function_configuration fails
        while not runtime_set and count < LambdaArgsObject.retry_attempts:
            count += 1
            time.sleep(5)
            try:
                response = self.client.update_function_configuration(
                    FunctionName=LambdaArgsObject.function_name,
                    Runtime=f'python3.{LambdaArgsObject.python3_minor_version}'
                )
                if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                    self.logger.info(f'update_function_configuration response: {response}')
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceConflictException':
                    if not LambdaArgsObject.mute:
                        logger.info('Lambda in pending state, waiting and retrying configuration update')
                    continue
                else:
                    raise e
            if not LambdaArgsObject.mute:
                logger.info('Lambda configuration updated: runtime set')
            runtime_set = True

        if not runtime_set:
            raise Exception(f'Unable to set runtime for function {LambdaArgsObject.function_name}')

        if not LambdaArgsObject.mute:
            logger.info(f'Lambda {LambdaArgsObject.function_name} runtime set to python3.{LambdaArgsObject.python3_minor_version}')

        return True

    def lambda_update_code(self, **kwargs):
        LambdaArgsObject = LambdaUpdateArgs()
        LambdaArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(LambdaArgsObject.function_name, str):
            raise ValueError(f'Invalid input function_name `{LambdaArgsObject.function_name}`, must be a string.')

        if not isinstance(LambdaArgsObject.verbose, bool):
            raise ValueError(f'Invalid input verbose `{LambdaArgsObject.verbose}`, must be a Boolean.')

        if not isinstance(LambdaArgsObject.mute, bool):
            raise ValueError(f'Invalid input mute `{LambdaArgsObject.mute}`, must be a Boolean.')

        self.archive_create(
            function_name=LambdaArgsObject.function_name,
            mute=LambdaArgsObject.mute
        )

        code_updated = False
        count = 0
        # if lambda is in update/pending state update_function_code fails
        while not code_updated and count < AWS_ACTION_RETRY_ATTEMPTS_DEFAULT:
            count += 1
            time.sleep(5)
            try:
                response = self.client.update_function_code(
                    FunctionName=LambdaArgsObject.function_name,
                    ZipFile=self.zip_bytes,
                    Publish=False,
                    DryRun=LambdaArgsObject.dry_run
                )
                if not LambdaArgsObject.mute and LambdaArgsObject.verbose:
                    logger.info(f'update_function_configuration response: {response}')
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceConflictException':
                    if not LambdaArgsObject.mute:
                        logger.info('Lambda in pending state, waiting and retrying code update')
                    continue
                else:
                    raise e

            code_updated = True
            if not LambdaArgsObject.mute:
                logger.info(f'Updated function {LambdaArgsObject.function_name} code')

        if not code_updated:
            raise Exception(f'Unable to update function {LambdaArgsObject.function_name}')

        return True

    def _layer_arns_list_generate(self, layer_names):
        layer_arns = []
        layers_config = self._load_layers_dependencies_config()
        for layer_identifier in layer_names:
            layer_config = layers_config.get(layer_identifier, None)
            if layer_config is not None:
                layer_name = layer_config.get('name', None)
                if not layer_name:
                    continue
                # get version from configuration in dependencies file first
                layer_version = layer_config.get('version', None)
                # if version not available and global dependency then fetch latest version
                if not layer_version:
                    if layer_identifier not in GLOBAL_DEPENDENCIES_LAYER_IDENTIFIERS:
                        continue
                    layer_version = self.get_latest_global_dependencies_layer_version()
                if layer_version:
                    layer_arns.append(f'{LAYER_ARN_BASE}{layer_name}:{layer_version}')

        return layer_arns

    def _layers_add_to_lambda(self, function_name, verbose=False, mute=False):
        if mute:
            logger.setLevel(logging.ERROR)

        logger.info(f'Attaching layers to function: {function_name}')
        layer_names = self._create_function_layers_list(function_name)
        layer_arns = self._layer_arns_list_generate(layer_names)

        layers_added = False
        count = 0
        # lambda is in pending state upon creation until fully setup
        # update_function_configuration fails when the lambda is pending...
        while not layers_added and count < 24:
            count += 1
            time.sleep(5)
            try:
                # run update-function-configuration to add the layers
                # adding a new layers list will overwrite existing layers list
                response = self.client.update_function_configuration(
                    FunctionName=function_name,
                    Layers=layer_arns
                )
                if verbose:
                    logger.debug(f'update_function_configuration response:\n\n{json.dumps(response)}\n')
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceConflictException':
                    logger.info('Lambda in pending state, waiting and retrying layers update')
                    continue
                else:
                    raise Exception from e

            layers_added = True

        if not layers_added:
            raise Exception(f'Unable to add layers to function {function_name}')

        if not mute:
            logger.info(f'Attached layers to function {function_name}')
        return True

    def _layers_for_function(self, function_name, function_config, common_config):
        layers = []

        # all lambdas get the global dependencies layer
        layers.append('global_dependencies')

        # common dependencies
        for dependency in function_config.get('common_dependencies', []):
            config = common_config.get(dependency, None)
            if config is None:
                raise KeyError(f'Undefined common dependency in {function_name}: {dependency}')
            dependency_layer_name = config.get('layer', None)
            if dependency_layer_name is not None:
                layers.append(dependency_layer_name)

        # direct dependencies
        for config in function_config.get('dependencies', []):
            dependency_layer_name = config.get('layer', None)
            if dependency_layer_name is not None:
                layers.append(dependency_layer_name)

        # de-duplicate
        layers = list(set(layers))

        return layers

    def list_layer_versions(self, layer_name, verbose=False, mute=False):
        response = None
        layer_versions = []

        if not mute:
            logger.info(f"Listing layers for '{layer_name}'...")
        try:
            response = self.client.list_layer_versions(
                LayerName=layer_name
            )
            if not mute and verbose:
                logger.info(f'list_layer_versions response: {response}')
        except Exception as e:
            if not mute:
                logger.warning(f'list_layer_versions for {layer_name} failed: {e}')
            return False
        finally:
            self.client_close()

        if response is not None:
            layer_versions = response.get('LayerVersions')
            self.layers[layer_name] = layer_versions

        return layer_versions

    def _load_layers_dependencies_config(self):
        dependencies = bundle.json_load_dependencies()

        return dependencies.get('layers', {})


class LambdaApiGatewayService(LambdaService):
    global logger

    ACTION = 'lambda:InvokeFunction'
    PRINCIPAL = 'apigateway.amazonaws.com'

    API_ARN_TEMPLATE = 'arn:aws:execute-api:{}:{}:{}/*/{}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def api_arn_build(self, region, account_id, api_id, request_path):
        return self.API_ARN_TEMPLATE.format(region, account_id, api_id, request_path)

    def policy_deploy(self, **kwargs):
        ArgsObject = LambdaApiGatewayArgs()
        ArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(ArgsObject.lambda_arn, str):
            raise ValueError(f'Invalid input: lambda_arn `{ArgsObject.lambda_arn}`, must be a string.')

        if not isinstance(ArgsObject.api_arn, str):
            raise ValueError(f'Invalid input: api_arn `{ArgsObject.api_arn}`, must be a string.')

        if not isinstance(ArgsObject.mute, bool):
            raise ValueError(f'Invalid input: mute `{ArgsObject.mute}`, must be a Boolean.')

        if not ArgsObject.mute:
            logger.info('Deploying policy...')

        try:
            policy_response = self.client.add_permission(
                FunctionName=ArgsObject.lambda_arn,
                StatementId=str(f'arcimoto-lambda-utility-grant-api-{uuid.uuid4()}'),
                Action=self.ACTION,
                Principal=self.PRINCIPAL,
                SourceArn=ArgsObject.api_arn
            )
        except Exception as e:
            if not ArgsObject.mute:
                logger.error(f'Failed to deploy policy for function {ArgsObject.lambda_arn}: {e}')
            raise e

        if not ArgsObject.mute:
            if ArgsObject.verbose:
                logger.info(f'Deploy policy response:\n\n{json.dumps(policy_response, indent=2)}\n')
            logger.info('Policy deployed successfully')
        return True

    def policy_exists(self, **kwargs):
        ArgsObject = LambdaApiGatewayArgs()
        ArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(ArgsObject.lambda_arn, str):
            raise ValueError(f'Invalid input: lambda_arn `{ArgsObject.lambda_arn}`, must be a string.')

        if not isinstance(ArgsObject.api_arn, str):
            raise ValueError(f'Invalid input: api_arn `{ArgsObject.api_arn}`, must be a string.')

        if not isinstance(ArgsObject.mute, bool):
            raise ValueError(f'Invalid input: mute `{ArgsObject.mute}`, must be a Boolean.')

        policy = self.policy_get(lambda_arn=ArgsObject.lambda_arn)
        if policy is False:
            return False
        for statement in policy.get('Statement', []):
            if statement.get('Action', '') == self.ACTION and \
                    statement.get('Principal', {}).get('Service', '') == self.PRINCIPAL and \
                    statement.get('Resource', '') == ArgsObject.lambda_arn and \
                    statement.get('Condition', {}).get('ArnLike', {}).get('AWS:SourceArn', '') == ArgsObject.api_arn:
                return True
        return False

    def policy_get(self, **kwargs):
        ArgsObject = LambdaApiGatewayArgs()
        ArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(ArgsObject.lambda_arn, str):
            raise ValueError(f'Invalid input: lambda_arn `{ArgsObject.lambda_arn}`, must be a string.')

        if not isinstance(ArgsObject.mute, bool):
            raise ValueError(f'Invalid input: mute `{ArgsObject.mute}`, must be a Boolean.')

        try:
            policy_response = self.client.get_policy(
                FunctionName=ArgsObject.lambda_arn
            )
            if not ArgsObject.mute and ArgsObject.verbose:
                logger.info(f'Policy response:\n\n{json.dumps(policy_response, indent=2)}\n')
            return json.loads(policy_response.get('Policy'))
        except self.client.exceptions.ResourceNotFoundException:
            # get_policy returns ResourceNotFoundException if there is no policy attached to the lambda
            return False
        except Exception as e:
            if not ArgsObject.mute:
                logger.error(f'Failed to read policy for function {ArgsObject.lambda_arn}: {e}')
            raise e


class LambdaLayersService(LambdaService):
    global logger

    layer_description = None
    layer_name = None
    layer_identifier = None
    layer_packages = None
    layer_config = None
    layers_config = None
    zip_bytes = None

    def __init__(self, layer_identifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layer_identifier_set(layer_identifier)
        self._layer_config_get()

    def _archive_create(self):
        zip_path = self._create_layer_bundle(self.layer_identifier, self.layer_config)
        with open(zip_path, 'rb') as f:
            self.zip_bytes = f.read()
        return self.zip_bytes

    def _assets_for_layer(self, layer_name, layer_config):
        layer_assets = []
        (functions_config, common_config, global_config) = bundle.load_dependencies()
        global_dependencies_layer_names = [
            'global_dependencies',
            'global_dependencies_dev',
            'global_dependencies_staging',
            'global_dependencies_test'
        ]

        if layer_name in global_dependencies_layer_names:
            for dependency in global_config:
                layer_assets.append(global_config[dependency])
        else:
            # common dependencies
            layer_packages = layer_config.get('meta', {}).get('contains', [])
            if len(layer_packages) == 0:
                raise Exception(f'No layer packages found in common_dependencies for {layer_name}')
            # use packages in meta:contains property to assemble assets
            for dependency in common_config:
                if dependency in layer_packages:
                    layer_assets.append({**common_config[dependency], **{'name': dependency}})
            # ignore local dependencies

        if len(layer_assets) == 0:
            raise Exception(f'No layer assets assembled for {layer_name}')

        return layer_assets

    def _create_layer_bundle(self, layer_name, layer_config):
        global logger

        layer_assets = self._assets_for_layer(layer_name, layer_config)
        # use layer_assets to build bundle
        build_dir = tempfile.TemporaryDirectory()
        compatible_runtimes = layer_config.get('meta', {}).get('compatible_runtimes', [])
        if len(compatible_runtimes) == 0:
            raise KeyError(f'No compatible_runtimes set in layer config in dependencies.json for {layer_name}')
        for runtime in compatible_runtimes:
            # needs folder structure(s) to match expected python runtime location(s)
            directory = path.clamp_path_to_root(f'python/lib/{runtime}/site-packages/', build_dir.name)
            bundle.assemble_assets(layer_assets, directory, True)

        return path.create_archive(build_dir.name)

    def _layer_config_get(self):
        self.layers_config = self._load_layers_dependencies_config()

        self.layer_config = self.layers_config.get(self.layer_identifier, None)
        if self.layer_config is None:
            raise KeyError(f'No layer config found in dependencies.json for `{self.layer_identifier}`\n{self.layers_config}')

        self.layer_name = self.layer_config.get('name', None)
        if self.layer_name is None:
            raise KeyError(f'No layer name property in config `{self.layer_name}`:\n{self.layer_config}')

        self.layer_packages = self.layer_config.get('meta', {}).get('contains', [])

    def _layer_description_set(self, description_addendum=None):
        self.layer_description = f'contains: [{", ".join(self.layer_packages)}]'
        if description_addendum is not None:
            self.layer_description = f'{self.layer_description}, description: {description_addendum}'

    def _layer_identifier_set(self, value):
        if not isinstance(value, str):
            raise ValueError(f'Invalid input: layer_identifier `{value}`, must be a string.')
        self.layer_identifier = value

    def _layer_publish_version(self, **kwargs):
        ArgsObject = LambdaLayersArgs()
        ArgsObject._set_attributes_from_kwargs(kwargs)

        # input validation
        if not isinstance(ArgsObject.mute, bool):
            raise ValueError(f'Invalid input: mute `{ArgsObject.mute}`, must be a Boolean.')

        try:
            response = self.client.publish_layer_version(
                LayerName=self.layer_name,
                Description=self.layer_description,
                Content={'ZipFile': self.zip_bytes},
                CompatibleRuntimes=ArgsObject.compatible_runtimes,
                LicenseInfo=ArgsObject.license_info
            )
            self.arn = response.get('LayerVersionArn', None)
        except ParamValidationError as e:
            raise e
        except Exception as e:
            raise Exception(f'Unable to publish layer version: {e}') from e

        if not ArgsObject.mute:
            logger.warning(f'Created layer `{self.layer_name}` version with ARN `{self.arn}`')

        return self.arn

    def publish_layer_version(self, **kwargs):
        ArgsObject = LambdaLayersArgs()
        ArgsObject._set_attributes_from_kwargs(kwargs)

        self._layer_description_set(ArgsObject.description)
        self._archive_create()
        return self._layer_publish_version(
            mute=ArgsObject.mute
        )


class LambdaArgs:
    ''' Used to pass into commands to allow setting of attributes '''

    account_id = DEFAULT_AWS_ACCOUNT_ID
    alias = None
    description = None
    dry_run = False
    env = None
    function = None
    mute = False
    region = DEFAULT_AWS_REGION
    retry_attempts = None
    verbose = False
    version = None
    zip_bytes = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._alias_set()
        self.retry_attempts_set()

    def _alias_set(self, value=DEV_ALIAS):
        self.alias = value

    def account_id_set(self, account_id=DEFAULT_AWS_ACCOUNT_ID):
        self.account_id = account_id

    def _description_set(self, value=''):
        self.description = value

    def dry_run_set(self, dry_run=False):
        self.dry_run = dry_run

    def env_set(self, env=DEV_ALIAS):
        self.env = env

    @property
    def function_name(self):
        return self.function

    @function_name.setter
    def function_name(self, value):
        self.function = value

    def function_name_set(self, function_name):
        self.function = function_name

    def mute_set(self, mute=False):
        self.mute = mute

    def region_set(self, region=DEFAULT_AWS_REGION):
        self.region = region

    def retry_attempts_set(self, value=AWS_ACTION_RETRY_ATTEMPTS_DEFAULT):
        self.retry_attempts = value

    def _set_attributes_from_kwargs(self, input_kwargs):
        # set up args object from input kwargs
        for key, value in input_kwargs.items():
            if value is not None:
                setattr(self, key, value)
        return self

    def verbose_set(self, verbose=False):
        self.verbose = verbose

    def _version_set(self, value='$LATEST'):
        self.version = value

    def _zip_bytes_set(self, value):
        self.zip_bytes = value


class LambdaCreateArgs(LambdaArgs):
    ''' Used to pass into commands to allow setting of attributes '''

    alias = DEV_ALIAS
    description = None
    python3_minor_version = PYTHON3_MINOR_VERSION_DEFAULT
    role = None
    tag = []
    tags = {}
    timeout = LAMBDA_DEFAULT_TIMEOUT
    vpc = 'main'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def description_set(self, description=''):
        self.description = description

    def python3_minor_version_set(self, minor_version=PYTHON3_MINOR_VERSION_DEFAULT):
        global PYTHON3_ALLOWED_MINOR_VERSIONS
        if minor_version not in PYTHON3_ALLOWED_MINOR_VERSIONS:
            raise ValueError(f'Input {minor_version} not in allowed versions {PYTHON3_ALLOWED_MINOR_VERSIONS}')
        self.python3_minor_version = minor_version

    def role_set(self, role):
        self.role = role

    def tag_set(self, tag):
        self.tag = tag

    def tags_set(self, tags):
        self.tags = tags

    def timeout_set(self, timeout=LAMBDA_DEFAULT_TIMEOUT):
        if timeout < 1:
            raise ValueError('Input timeout must be a positive, non-zero integer.')
        self.timeout = timeout

    def vpc_set(self, vpc=LAMBDA_DEFAULT_VPC):
        global LAMBDA_ALLOWED_VPCS
        if vpc not in LAMBDA_ALLOWED_VPCS:
            raise ValueError(f'Input vpc must be one of {LAMBDA_ALLOWED_VPCS}')
        self.vpc = vpc


class LambdaApiGatewayArgs(LambdaArgs):

    api_arn = None
    lambda_arn = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def api_arn_set(self, api_arn):
        self.api_arn = api_arn

    def lambda_arn_set(self, lambda_arn):
        self.lambda_arn = lambda_arn


class LambdaInvokeArgs(LambdaArgs):

    payload = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def client_id_set(self, client_id=DEFAULT_CLIENT_ID):
        self.client_id = client_id

    @property
    def cognito_client_id(self):
        return DEFAULT_CLIENT_ID

    def password_set(self, password):
        self.password = password

    def payload_set(self, payload={}):
        self.payload = payload

    def user_set(self, username):
        self.user = username


class LambdaLayersArgs(LambdaArgs):

    compatible_runtimes = None
    layer_description = None
    layer_name = None
    license_info = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._compatible_runtimes_set()
        self._license_info_set()

    @property
    def description(self):
        return self.layer_description

    @description.setter
    def description(self, value):
        self.layer_description = value

    def _compatible_runtimes_set(self, value=LAMBDA_LAYERS_COMPATIBLE_RUNTIMES):
        self.compatible_runtimes = value

    def _layer_description_set(self, value):
        self.layer_description = value

    def _layer_name_set(self, value):
        self.layer_name = value

    def _license_info_set(self, value=LICENSE_DEFAULT):
        self.license_info = value


class LambdaRuntimeArgs(LambdaArgs):

    python3_minor_version = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._python3_minor_version_set()

    def _python3_minor_version_set(self, value=PYTHON3_MINOR_VERSION_DEFAULT):
        self.python3_minor_version = value


class LambdaTestArgs(LambdaArgs):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id_set()

    def client_id_set(self, client_id=DEFAULT_CLIENT_ID):
        self.client_id = client_id

    @property
    def cognito_client_id(self):
        return DEFAULT_CLIENT_ID


class LambdaUpdateArgs(LambdaArgs):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
