import io

from setuptools import find_packages, setup

setup(
    name='opvoeden-api-client',
    version='1.0.0.dev0',
    description='Client for Stichting Opvoeden API V1',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    keywords=['stichting', 'opvoeden', 'api', 'client', 'rest'],
    author='Jaap Roes (Leukeleu)',
    author_email='jroes@leukeleu.nl',
    maintainer='Leukeleu',
    maintainer_email='info@leukeleu.nl',
    url='https://github.com/leukeleu/opvoeden-api-client',
    packages=find_packages(exclude=['tests']),
    install_requires=['requests'],
    classifiers=[],
    license='',
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)
