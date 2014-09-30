try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='CS50',
    version='0.2',
    author='Dan Armendariz',
    author_email='danallan@cs.harvard.edu',
    packages=['library50'],
    url='http://pypi.python.org/pypi/CS50/',
    license='LICENSE.txt',
    description='Utilities for OpenID with Python and CS50 ID.',
    keywords = ['cs50'],
    install_requires=[
        "python-openid>=2.2.5"
    ],
)
