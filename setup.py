# -*- coding: utf-8 -*-
########################################################################
#
#       License: BSD 3-clause
#       Created: September 22, 2010
#       Author:  Francesc Alted - faltet@gmail.com
#
########################################################################

# flake8: noqa

from __future__ import print_function

import os
import platform
import re
import sys
import io

from skbuild import setup
from glob import glob
from distutils.version import LooseVersion
from distutils.command.build_ext import build_ext
from distutils.errors import CompileError
from textwrap import dedent


if __name__ == '__main__':

    with io.open('README.rst', encoding='utf-8') as f:
        long_description = f.read()

    try:
        import cpuinfo
        cpu_info = cpuinfo.get_cpu_info()
    except Exception:
        # newer cpuinfo versions fail to import on unsupported architectures
        cpu_info = None

    ########### Check versions ##########
    def exit_with_error(message):
        print('ERROR: %s' % message)
        sys.exit(1)

    # Check for Python
    if sys.version_info[0] == 2:
        if sys.version_info[1] < 7:
            exit_with_error("You need Python 2.7 or greater to install blosc!")
    elif sys.version_info[0] == 3:
        if sys.version_info[1] < 4:
            exit_with_error("You need Python 3.4 or greater to install blosc!")
    else:
        exit_with_error("You need Python 2.7/3.4 or greater to install blosc!")

    tests_require = ['numpy', 'psutil']

    ########### End of checks ##########

    # Read the long_description from README.rst
    with open('README.rst') as f:
        long_description = f.read()

    # Blosc version
    VERSION = open('VERSION').read().strip()
    # Create the version.py file
    open('blosc/version.py', 'w').write('__version__ = "%s"\n' % VERSION)

    # Allow setting the Blosc dir if installed in the system
    BLOSC_DIR = os.environ.get('BLOSC_DIR', '')

    # Check for USE_CODEC environment variables
    try:
        INCLUDE_LZ4 = os.environ['INCLUDE_LZ4'] == '1'
    except KeyError:
        INCLUDE_LZ4 = True
    try:
        INCLUDE_SNAPPY = os.environ['INCLUDE_SNAPPY'] == '1'
    except KeyError:
        INCLUDE_SNAPPY = False  # Snappy is disabled by default
    try:
        INCLUDE_ZLIB = os.environ['INCLUDE_ZLIB'] == '1'
    except KeyError:
        INCLUDE_ZLIB = True
    try:
        INCLUDE_ZSTD = os.environ['INCLUDE_ZSTD'] == '1'
    except KeyError:
        INCLUDE_ZSTD = True

    classifiers = dedent("""\
    Development Status :: 5 - Production/Stable
    Intended Audience :: Developers
    Intended Audience :: Information Technology
    Intended Audience :: Science/Research
    License :: OSI Approved :: BSD License
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: System :: Archiving :: Compression
    Operating System :: Microsoft :: Windows
    Operating System :: Unix
    """)

    setup(name = "blosc",
        version = VERSION,
        description = 'Blosc data compressor',
        long_description = long_description,
        classifiers = [c for c in classifiers.split("\n") if c],
        author = 'Francesc Alted, Valentin Haenel',
        author_email = 'faltet@gmail.com, valentin@haenel.co',
        maintainer = 'Francesc Alted, Valentin Haenel',
        maintainer_email = 'faltet@gmail.com, valentin@haenel.co',
        url = 'http://github.com/blosc/python-blosc',
        license = 'https://opensource.org/licenses/BSD-3-Clause',
        platforms = ['any'],
        tests_require=tests_require,
        zip_safe=False,
        packages = ['blosc'],
        )
elif __name__ == '__mp_main__':
    # This occurs from `cpuinfo 4.0.0` using multiprocessing to interrogate the 
    # CPUID flags
    # https://github.com/workhorsy/py-cpuinfo/issues/108
    pass
