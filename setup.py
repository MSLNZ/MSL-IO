import re
import sys
from distutils.cmd import Command
from setuptools import setup, find_packages


class ApiDocs(Command):
    """
    A custom command that calls sphinx-apidoc
    see: http://www.sphinx-doc.org/en/latest/man/sphinx-apidoc.html
    """
    description = 'builds the api documentation using sphinx-apidoc'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sphinx
        from sphinx.apidoc import main

        command = [
            None,  # in Sphinx < 1.7.0 the first command-line argument was parsed, in 1.7.0 it became argv[1:]
            '--force',  # overwrite existing files
            '--module-first',  # put module documentation before submodule documentation
            '--separate',  # put documentation for each module on its own page
            '-o', './docs/_autosummary',  # where to save the output files
            'msl',  # the path to the Python package to document
        ]

        if sphinx.version_info[:2] >= (1, 7):
            command.pop(0)

        main(command)
        sys.exit(0)


class BuildDocs(Command):
    """
    A custom command that calls sphinx-build
    see: http://www.sphinx-doc.org/en/latest/man/sphinx-build.html
    """
    description = 'builds the documentation using sphinx-build'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sphinx

        command = [
            None,  # in Sphinx < 1.7.0 the first command-line argument was parsed, in 1.7.0 it became argv[1:]
            '-b', 'html',  # the builder to use, e.g., create a HTML version of the documentation
            '-a',  # generate output for all files
            '-E',  # ignore cached files, forces to re-read all source files from disk
            'docs',  # the source directory where the documentation files are located
            './docs/_build/html',  # where to save the output files
        ]

        if sphinx.version_info[:2] < (1, 7):
            from sphinx import build_main  # Sphinx also changed the location of build_main
        else:
            from sphinx.cmd.build import build_main
            command.pop(0)

        build_main(command)
        sys.exit(0)


def read(filename):
    with open(filename) as fp:
        text = fp.read()
    return text


def fetch_init(key):
    # open the __init__.py file to determine the value instead of importing the package to get the value
    init_text = read('msl/io/__init__.py')
    return re.compile(r'{}\s*=\s*(.*)'.format(key)).search(init_text).group(1)[1:-1]


testing = {'test', 'tests', 'pytest'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if testing else []

needs_sphinx = {'doc', 'docs', 'apidoc', 'apidocs', 'build_sphinx'}.intersection(sys.argv)
sphinx = ['sphinx', 'sphinx_rtd_theme'] if needs_sphinx else []

setup(
    name='msl-io',
    version=fetch_init('__version__'),
    author=fetch_init('__author__'),
    author_email='joe.borbely@gmail.com',
    url='https://github.com/MSLNZ/msl-io',
    description='Write a short description about msl-io here',
    long_description=read('README.rst'),
    platforms='any',
    license='MIT',
    classifiers=[],  # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    setup_requires=sphinx + pytest_runner,
    tests_require=['pytest-cov', 'pytest'],
    install_requires=[],  # specify the packages that io depends on
    cmdclass={'docs': BuildDocs, 'apidocs': ApiDocs},
    packages=find_packages(include=('msl*',)),
    include_package_data=True,  # includes all files specified in MANIFEST.in when building the distribution
)