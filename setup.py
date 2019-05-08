import setuptools
import unittest


if __name__ == '__main__':
    with open('README.md', 'r') as fh:
        long_description = fh.read()

    setuptools.setup(
        name='stefanutils',
        version='0.0.1',
        author='Stefan',
        author_email='stefdoerr@gmail.com',
        description='My utilities',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/stefdoerr/utilities/',
        classifiers=[
            'Programming Language :: Python :: 3.6',
            'Operating System :: POSIX :: Linux',
        ],

        packages=setuptools.find_packages(include=['stefanutils*'], exclude=[]),

        install_requires=[
            'peewee',
            'natsort',
            'moleculekit',

        ],

        entry_points = {
            'console_scripts': ['vmdall=stefanutils.vmdall:main', 'pm=stefanutils.pm:main'],
        }
    )