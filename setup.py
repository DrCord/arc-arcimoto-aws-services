import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# maintained automatically in pipeline release to master branch by python-semantic-version
__version__ = '1.1.7'

setuptools.setup(
    name='arcimoto-aws-services',
    version=__version__,
    author='Cord Slatton',
    author_email='cords@arcimoto.com',
    description='Library for interacting with Arcimoto AWS services. Used in other repos as a dependency/submodule.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/arcimotocode1/arcimoto-aws-services',
    license='private',
    packages=[
        'arcimoto_aws_services'
    ],
    install_requires=[
        'boto3',
        'botocore',
        'cognito',
        'datetime',
        'jsonschema',
        'path',
        'uuid'
    ]
)
