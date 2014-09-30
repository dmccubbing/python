CS50 Library (Python)
============

Instructions adapted from [http://peterdowns.com/posts/first-time-with-pypi.html](this tutorial).

Preparation:

1. Create accounts on [http://pypi.python.org/pypi?%3Aaction=register_form](PyPI Live) and [http://testpypi.python.org/pypi?%3Aaction=register_form](PyPI Test).
1. Add the following to a `.pypirc` configuration file (recommended but not required):

    [distutils] # this tells distutils what package indexes you can push to
    index-servers =
        pypi
        pypitest

    [pypi] # authentication details for live PyPI
    repository: https://pypi.python.org/pypi
    username: {{pypi_username}}
    password: {{pypi_password}}

    [pypitest] # authentication details for test PyPI
    repository: https://testpypi.python.org/pypi
    username: {{pypitest_username}}
    password: {{pypitest_password}}

Deployment:

1. Ask danallan or cogden to add you as a maintainer to the CS50 PyPI package.
1. Update the code, readme, license, etc, as appropriate
1. Test deployment to PyPI test:

    python setup.py register -r pypitest # register pkg with test server
    python setup.py sdist upload -r pypitest # upload pkg to test server

1. If all goes well, deploy to prod:

    python setup.py register -r pypi # register pkg with pypi
    python setup.py sdist upload -r pypi # upload pkg to pypi

