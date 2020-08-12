from setuptools import setup, find_packages

setup(
    name = 'INSTApi', 
    version = '0.0.1', 
    packages = ['INSTApi'] + ['INSTApi.' + pack for pack in find_packages(where = 'INSTApi')],
    install_requires = [
        'requests',
    ]
)