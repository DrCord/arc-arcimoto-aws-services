import logging
import os.path
import tempfile
import zipfile


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


DEPENDENCIES_CONFIG = "dependencies.json"
DEPENDENCIES_CONFIG_SCHEMA = "dependencies.schema.json"
BUNDLE_CONFIG_SCHEMA = "bundle.schema.json"
LAMBDA_SOURCE_DIR = "lambda"

ROOT_PATH_LINUX = '/'
ROOT_PATH_WINDOWS = 'c:\\'


def find_root_directory_path():
    """
    Walks up the directory tree starting from the currently executing file looking
    for the DEPENDENCIES_CONFIG file. Returns the directory if found, None otherwise.
    """
    path = os.path.abspath(os.path.dirname(__file__))
    while path.lower() not in [ROOT_PATH_LINUX, ROOT_PATH_WINDOWS]:
        if os.path.exists(os.path.join(path, DEPENDENCIES_CONFIG)):
            return path
        (path, current_dir) = os.path.split(path)

    # unable to get root dir from __file__, probably due to module running installed vs locally
    # use current working directory as root directory
    return os.getcwd()


def clamp_path_to_root(path, root):
    """
    Ensures the requested path is properly rooted to the root path, whether the
    path is a fragment, relative, or absolute.
    """
    cleaned_root = root
    if not os.path.isdir(cleaned_root):
        cleaned_root = os.path.dirname(cleaned_root)

    if path is None or path == "":
        return cleaned_root

    relative_path = path
    if os.path.isabs(relative_path):
        relative_path = os.path.relpath(relative_path, "/")

    return os.path.join(cleaned_root, relative_path)


def create_archive(source_dir):
    """
    Creates a zip archive of the specified source directory. Returns a path
    to a temp file containing the completed archive.
    """
    zip_file_path = tempfile.NamedTemporaryFile(delete=False)
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            path = os.path.join(root, file)
            relative_path = os.path.relpath(path, source_dir)
            zip_file.write(path, arcname=relative_path)

    zip_file.close()

    return zip_file_path.name
