from setuptools import setup

__version__ = '0.1.0'

setup(
        name='BootstrapWrapper',
        version='0.1.0',

        description='Dominate Bootstrap Wrapper',
        long_description=open('README.md').read(),

        author='Michael Housh',
        author_email='mhoush@houshhomeenergy.com',
        url='https://github.com/m-housh/bootstrap_wrapper.git',
        packages=['bootstrap_wrapper'],
        install_requires=['dominate', 'wtforms'],
    )

