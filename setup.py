"""Package configuration for hypergraphical."""
import os
from setuptools import find_packages, setup


def read(filename):
    """Read file contents."""
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), filename))
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')


dependencies = read('requirements.txt').split()
setup(
    name='hypergraphical',
    version='0.1',
    description='A Python package for generating transcriptions.',
    url='https://github.com/NickolasHKraus/hypergraphical',
    author='Nickolas Kraus <0x@nickolaskraus.io>',
    install_requires=dependencies,
    packages=find_packages(exclude=['*.test', '*.test.*', 'test.*', 'test']),
    entry_points={
        'console_scripts': ['hypergraphical=hypergraphical.cli:cli'],
    },
    include_package_data=True,
    zip_safe=False)
