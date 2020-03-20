
from setuptools import setup, find_packages
from systematic_files.version import __version__

setup(
    name='systematic-files',
    keywords='system management files mounts patterns',
    description='Filesystem utilities for systematic',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://git.tuohela.net/systematic-components/systematic-files',
    version=__version__,
    license='PSF',
    python_requires='>3.6.0',
    packages=find_packages(),
    install_requires=(
        'systematic-cli>=20200320.1',
    ),
    tests_require=(
        'pytest-cov',
        'pytest-datafiles',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
