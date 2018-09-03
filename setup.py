"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages
from distutils.core import setup

from thermos import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=thermos', '--cov-report=term-missing'])
        raise SystemExit(errno)

setup(
    name = 'thermos',
    version = __version__,
    description = 'A command line program in Python for creating flask standard application structure, blueprints and templates.',
    long_description = long_description,
    url = 'https://github.com/zecollokaris/Thermos-cli',
    author = 'Mwangi Njuguna <mwanginjuguna59@gmail.com>,Christine Karimi <karimikim3@gmail.com>,Faith Thuita <thuitamuthoni15@gmail.com>,Collins Kariuki <collo.kariss@gmail.com>',
    maintainer = 'Mwangi Njuguna, Collins Kariuki',
    maintainer_email = 'mwanginjuguna59@gmail.com , collo.kariss@gmail.com',
    license = 'MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Flask Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
    ],
    keywords = 'flask,cli',
    packages=['thermos'],
    #package_dir = {'': '/lib'},
    install_requires = ['docopt','colorama','termcolor'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'thermos=thermos.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
