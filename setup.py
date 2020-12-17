
from setuptools import setup, find_packages
from pathlib_tree import __version__

setup(
    name='pathlib-tree',
    keywords='system management files trees mounts patterns',
    description='Filesystem tree utilities',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://git.tuohela.net/python/pathlib-tree',
    version=__version__,
    license='PSF',
    python_requires='>3.6.0',
    packages=find_packages(),
    entry_points={},
    install_requires=(
        'cli-toolkit>=1.0.2',
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
