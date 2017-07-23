import os
from setuptools import find_packages, setup

# Load README file for long description.
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Main setup and configuration.
setup(
    name='flask-jobaddservice',
    version='0.3.0',
    packages=find_packages(),
    include_package_data=True,
    license='Apache License Version 2.0',
    description='Job add service for Flask.',
    long_description=README,
    url='https://github.com/marcbperez/flask-jobaddservice',
    author='marcbperez',
    author_email='marcbperez@users.noreply.github.com',
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-oauthlib',
        'bcrypt',
        'pyopenssl',
        'flask-restful',
        'flask-cors',
        'requests',
        'lxml',
        'beautifulsoup4',
    ],
    setup_requires=[
        'pytest-runner<=3.9',
        'setuptools-pep8',
    ],
    tests_require=[
        'pep8',
        'pytest-cov',
        'pytest',  # Keep at the end to avoid conflicts.
    ],
)
