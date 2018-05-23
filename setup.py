from setuptools import setup

setup(
    name='canonicalwebteam.snapstoreapi',
    version='0.2',
    author='Canonical Webteam',
    author_email='thomas.bille@canonical.com',
    url='https://github.com/canonical-webteam/snapstore-api',
    license='AGPLv3',
    description='Snapstore API',
    packages=[
        'canonicalwebteam.snapstoreapi',
    ],
    install_requires=[
        "requests",
        "pymacaroons",
        "python-openid",
        "prometheus_client",
    ],
    # TODO Add proper test suite
    test_suite='tests.py',
)
