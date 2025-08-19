#!/usr/bin/env python3

"""The setup script."""

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open('README.md') as f:
    long_description = f.read()


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Topic :: Scientific/Engineering',
]

setup(
    name='portraitpy',
    description='portraitpy: Extending matplotlib to add support for portrait or Gleckler plots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    maintainer='Lukas Pilz',
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=install_requires,
    license='Apache 2.0',
    zip_safe=False,
    entry_points={},
    keywords='matplotlib, portrait, gleckler, portraitpy',
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
)
