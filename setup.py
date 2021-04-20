""" Project setup file """
from setuptools import find_packages, setup

setup(
    name='auth_demo',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'aniso8601==6.0.0',
        'astroid==2.2.5',
        'atomicwrites==1.3.0',
        'attrs==19.1.0',
        'bcrypt==3.1.6',
        'certifi==2019.3.9',
        'cffi==1.12.2',
        'chardet==3.0.4',
        'Click==7.0',
        'coverage==4.5.3',
        'Flask==1.0.2',
        'Flask-Bcrypt==0.7.1',
        'Flask-Jsonpify==1.5.0',
        'Flask-Login==0.4.1',
        'Flask-Restless==0.17.0',
        'Flask-SQLAlchemy==2.3.2',
        'Flask-Testing==0.7.1',
        'Flask-WTF',
        'idna==2.8',
        'isort==4.3.15',
        'itsdangerous==1.1.0',
        'Jinja2==2.10',
        'lazy-object-proxy==1.3.1',
        'MarkupSafe==1.1.1',
        'mccabe==0.6.1',
        'mimerender==0.6.0',
        'more-itertools==6.0.0',
        'nose',
        'pathlib2==2.3.3',
        'pluggy==0.9.0',
        'py==1.10.0',
        'pycparser==2.19',
        'python-dateutil==2.8.0',
        'python-mimeparse==1.6.0',
        'pytz==2018.9',
        'requests==2.21.0',
        'six==1.12.0',
        'SQLAlchemy==1.3.1',
        'typed-ast==1.3.1',
        'urllib3==1.24.1',
        'Werkzeug==0.14.1',
        'wrapt'
    ],
)
