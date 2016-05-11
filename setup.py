from setuptools import setup, find_packages
from kraken import __version__ as version

setup(
    name='kraken',
    version=version.__version__,
    py_modules=['kraken'],
    packages=find_packages(),
    url='bitbucket.org/leopepe/kraken',
    license='Simplified BSD',
    author='Leonardo Pepe',
    author_email='lpepefreitas@gmail.com',
    description='Kraken is a destructive EC2 client',
    include_package_data=True,
    install_requires=[
        'click',
        'boto3',
    ],
    entry_points='''
        [console_scripts]
        kraken=kraken.__main__:cli
    ''',
)
