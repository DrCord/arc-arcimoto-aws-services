import json
import logging
import os
import shutil
import tempfile
import zipfile

from arcimoto_aws_services import path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def assemble_assets(assets, build_dir, layer=False):

    root_dir = path.find_root_directory_path()

    for asset in assets:
        asset_action = asset.get('action', 'copy')
        asset_source = asset.get('from', None)
        asset_dest = asset.get('to', None)
        asset_name = asset.get('name', None)

        if asset_action not in ['copy', 'unzip']:
            raise ValueError('Values allowed for an asset action are `copy` and `unzip`')

        if asset_source is None:
            raise ValueError('Each asset must have a `from` property (source)')

        if not layer and asset_dest is None and asset_action != 'unzip':
            raise ValueError(f'Each asset using the `copy` action must have a `to` property (destination): {asset}')

        if layer and asset_name is None:
            raise ValueError(f'Each asset that uses a layer must have a `name` property: {asset}')

        source = path.clamp_path_to_root(asset_source, root_dir)
        dest = path.clamp_path_to_root(asset_dest, build_dir)

        if asset_action == 'copy':
            copy_asset(source, dest)
        elif asset_action == 'unzip':
            unzip_asset(source, dest)


def assets_for_function(function_name, function_config, common_config):
    assets = []
    # input validation
    if not isinstance(function_name, str) or function_name == '':
        raise ValueError('Input function_name must be a non-empty string')

    if not isinstance(function_config, dict) or len(function_config.keys()) == 0:
        raise ValueError('Input function_config must be a non empty dictionary')

    if not isinstance(common_config, dict) or len(common_config.keys()) == 0:
        raise ValueError('Input common_config must be a non empty dictionary')

    # pull in common dependencies
    for dependency in function_config.get('common_dependencies', []):
        config = common_config.get(dependency, None)
        if config is None:
            raise KeyError(f'Undefined common dependency `{dependency}` in `{function_name}` configuration')
        dependency_has_layer = config.get('layer', False)
        if not dependency_has_layer:
            assets.append(config)

    bundle = function_config.get('bundle', None)
    if bundle is None:
        raise ValueError(f'Lambda dependencies config for `{function_name}` does not have required `bundle` property')

    if bundle == 'debug':
        if function_name == 'util_authkey_execute_sql':
            bundle += '/authkey'
        elif function_name == 'util_telemetry_execute_sql':
            bundle += '/main'
        elif function_name == 'util_users_execute_sql':
            bundle += '/users'
    function_path = f'{path.LAMBDA_SOURCE_DIR}/{bundle}/{function_name}.py'

    # include {function_name}.py file from function's bundle folder
    assets.append({
        'from': function_path,
        'to': f'{path.LAMBDA_SOURCE_DIR}/{function_name}.py'
    })

    # include direct dependencies
    for config in function_config.get('dependencies', []):
        assets.append(config)

    # include bundle.json from function's bundle folder
    function_bundle = bundle.replace('/tests', '')
    assets.append({
        'from': f'{path.LAMBDA_SOURCE_DIR}/{function_bundle}/bundle.json',
        'to': 'bundle.json'
    })

    return assets


def bundle_info_get(lambda_name, bundle_name, bundle_json_file_path, mute=False):
    bundle_info = {}
    bundle_path = bundle_name
    file_path = None

    # input provided
    if bundle_json_file_path is not None:
        file_path = bundle_json_file_path
    else:  # default
        if bundle_name == 'debug':
            if lambda_name == 'util_authkey_execute_sql':
                bundle_path += '/authkey'
            elif lambda_name == 'util_telemetry_execute_sql':
                bundle_path += '/main'
            elif lambda_name == 'util_users_execute_sql':
                bundle_path += '/users'
        file_path = os.path.join(path.find_root_directory_path(), 'lambda', bundle_path, 'bundle.json')

    if os.path.exists(file_path):
        try:
            with open(file_path) as f:
                bundle_info = json.load(f)
        except Exception as e:
            if not mute:
                logger.warning(f'Unable to load bundle {bundle_name} bundle.json file from {file_path}: {e}')
    else:
        if not mute:
            logger.warning(f'bundle.json file for {bundle_name}:{lambda_name} not located at {file_path}')

    return (
        bundle_info
    )


def bundles_list():
    # generate list of bundles
    bundles = []
    dependencies = json_load_dependencies()
    function_definitions = dependencies.get('functions', {})
    for lambda_definition in function_definitions.values():
        bundle = lambda_definition.get('bundle', None)
        if bundle is not None:
            if not bundle.endswith('/tests'):
                bundles.append(bundle)
    if len(bundles):
        # de-duplicate
        bundles = list(set(bundles))
        bundles.sort()

    return bundles


def copy_asset(source, dest):
    global logger
    """
    Handle copying the specified from_path resource to to_path. Paths will be
    validated and must exist
    """
    if source is None:
        raise ValueError("No source file specified for copy action")
    if not os.path.exists(source):
        raise FileNotFoundError("Source file {} does not exist".format(source))

    if os.path.isdir(source):
        shutil.copytree(source, dest)

    else:
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        shutil.copyfile(source, dest)


def create_function_bundle(function_name):
    (functions, common_config, global_dependencies) = load_dependencies()
    function_config = functions.get(function_name, None)
    if function_config is None:
        raise KeyError(f'No configuration found for lambda {function_name}')

    assets = assets_for_function(function_name, function_config, common_config)

    build_dir = tempfile.TemporaryDirectory()
    assemble_assets(assets, build_dir.name)

    return path.create_archive(build_dir.name)


def json_load_bundle_json(bundle_name):
    bundle_json = {}
    with open(os.path.join('lambda', bundle_name, 'bundle.json')) as f:
        bundle_json = json.load(f)

    return bundle_json


def json_load_bundle_schema(bundle_schema_path=path.BUNDLE_CONFIG_SCHEMA):
    dependencies = {}
    with open(bundle_schema_path) as f:
        dependencies = json.load(f)

    return dependencies


def json_load_dependencies(dependencies_file_path=path.DEPENDENCIES_CONFIG):
    with open(dependencies_file_path) as f:
        dependencies = json.load(f)

    return dependencies


def json_load_dependencies_schema(dependencies_schema_path=path.DEPENDENCIES_CONFIG_SCHEMA):
    dependencies = {}
    with open(dependencies_schema_path) as f:
        dependencies = json.load(f)

    return dependencies


def lambda_bundle_get(lambda_name, dependencies_json_file_path=path.DEPENDENCIES_CONFIG):
    dependencies = json_load_dependencies(dependencies_json_file_path)
    bundle = dependencies.get('functions', {}).get(lambda_name, {}).get('bundle', None)

    return bundle


def load_dependencies():
    dependencies = json_load_dependencies()

    return (
        dependencies.get("functions", {}),
        dependencies.get("common_dependencies", {}),
        dependencies.get("global_dependencies", {})
    )


def unzip_asset(source, dest):
    """
    Handle decompressing a zip archive into the build directory. Paths will be
    validated and must exist
    """

    if source is None:
        raise ValueError("No source archive specified for zip action")
    if not os.path.exists(source):
        raise FileNotFoundError("Source archive {} does not exist".format(source))

    zip_ref = zipfile.ZipFile(source)
    zip_ref.extractall(dest)
    zip_ref.close()
