
from setuptools import setup, find_packages
from systematic_files import __version__

setup(
    name='systematic-files',
    keywords='system management files trees mounts patterns',
    description='Filesystem utilities for systematic',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://git.tuohela.net/systematic-components/systematic-files',
    version=__version__,
    license='PSF',
    python_requires='>3.6.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'treesync=systematic_files.bin.treesync.main:main',
        ],
    },
    install_requires=(
        'systematic-cli>=1.3.0',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
