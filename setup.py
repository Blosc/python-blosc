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

from setuptools import Extension
from setuptools import setup
from glob import glob
import cpuinfo

########### Check versions ##########
def exit_with_error(message):
    print('ERROR: %s' % message)
    sys.exit(1)

# Check for Python
if sys.version_info[0] == 2:
    if sys.version_info[1] < 6:
        exit_with_error("You need Python 2.6 or greater to install blosc!")
elif sys.version_info[0] == 3:
    if sys.version_info[1] < 3:
        exit_with_error("You need Python 3.3 or greater to install blosc!")
else:
    exit_with_error("You need Python 2.6/3.3 or greater to install blosc!")

tests_require = ['numpy']
if sys.version_info[:2] < (2, 7):
    tests_require += ['unittest2']

########### End of checks ##########

# Blosc version
VERSION = open('VERSION').read().strip()
# Create the version.py file
open('blosc/version.py', 'w').write('__version__ = "%s"\n' % VERSION)

# Global variables
CFLAGS = os.environ.get('CFLAGS', '').split()
LFLAGS = os.environ.get('LFLAGS', '').split()
# Allow setting the Blosc dir if installed in the system
BLOSC_DIR = os.environ.get('BLOSC_DIR', '')

# Handle --blosc=[PATH] --lflags=[FLAGS] --cflags=[FLAGS]
args = sys.argv[:]
for arg in args:
    if arg.find('--blosc=') == 0:
        BLOSC_DIR = os.path.expanduser(arg.split('=')[1])
        sys.argv.remove(arg)
    if arg.find('--lflags=') == 0:
        LFLAGS = arg.split('=')[1].split()
        sys.argv.remove(arg)
    if arg.find('--cflags=') == 0:
        CFLAGS = arg.split('=')[1].split()
        sys.argv.remove(arg)


# Blosc sources and headers

# To avoid potential namespace collisions use build_clib.py for each codec
# instead of co-compiling all sources files in one setuptools.Extension object.
clibs = [] # for build_clib, libraries TO BE BUILT

# Below are parameters for the Extension object
sources = ["blosc/blosc_extension.c"]
inc_dirs = []
lib_dirs = []
libs = []  # Pre-built libraries ONLY, like python36.so
def_macros = []
if BLOSC_DIR != '':
    # Using the Blosc library
    lib_dirs += [os.path.join(BLOSC_DIR, 'lib')]
    inc_dirs += [os.path.join(BLOSC_DIR, 'include')]
    libs += ['blosc']
else:
    # Libraries to be built with build_clib
    clibs.append( ('lz4', {'sources': glob('c-blosc/internal-complibs/lz4*/*.c')} ) )

    # Tried and failed to compile Snappy with gcc using 'cflags' on posix
    # setuptools always uses gcc instead of g++, as it only checks for the 
    # env var 'CC' and not 'CXX'.
    clibs.append( ('snappy', {'sources': glob('c-blosc/internal-complibs/snappy*/*.cc'), 
                               'cflags':'-std=c++11 -lstdc++' } ) )

    clibs.append( ('zlib', {'sources': glob('c-blosc/internal-complibs/zlib*/*.c')} ) )

    clibs.append( ('zstd', {'sources': glob('c-blosc/internal-complibs/zstd*/*/*.c'), 
                    'include_dirs': glob('c-blosc/internal-complibs/zstd*') + glob('c-blosc/internal-complibs/zstd*/common') } ) )
    # TODO: do we want env vars checks to disable libraries and macros?

    # Configure the Extension
    # Compiling everything from included C-Blosc sources
    sources += [f for f in glob('c-blosc/blosc/*.c')
                if 'avx2' not in f and 'sse2' not in f]

    inc_dirs += [os.path.join('c-blosc', 'blosc')]
    inc_dirs += glob('c-blosc/internal-complibs/*')
    inc_dirs += glob('c-blosc/internal-complibs/lz4*')
    inc_dirs += glob('c-blosc/internal-complibs/snappy*')
    inc_dirs += glob('c-blosc/internal-complibs/zstd*/common')
    inc_dirs += glob('c-blosc/internal-complibs/zstd*')
    
    # To undefine SNAPPY we have to not define the macro, as opposed to setting it to False
    def_macros += [('HAVE_LZ4', 1), ('HAVE_SNAPPY', 1), ('HAVE_ZLIB', 1), ('HAVE_ZSTD', 1) ]
    

    # Guess SSE2 or AVX2 capabilities
    cpu_info = cpuinfo.get_cpu_info()
    # SSE2
    if 'sse2' in cpu_info['flags']:
        print('SSE2 detected')
        CFLAGS.append('-DSHUFFLE_SSE2_ENABLED')
        sources += [f for f in glob('c-blosc/blosc/*.c') if 'sse2' in f]
        if os.name == 'posix':
            CFLAGS.append('-msse2')
        elif os.name == 'nt':
            def_macros += [('__SSE2__', 1)]
    # AVX2
    if 'avx2' in cpu_info['flags']:
        print('AVX2 detected')
        CFLAGS.append('-DSHUFFLE_AVX2_ENABLED')
        sources += [f for f in glob('c-blosc/blosc/*.c') if 'avx2' in f]
        if os.name == 'posix':
            CFLAGS.append('-mavx2')
        elif os.name == 'nt':
            def_macros += [('__AVX2__', 1)]
    # TODO: AVX512

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Archiving :: Compression
Operating System :: Microsoft :: Windows
Operating System :: Unix
"""

setup(name = "blosc",
      version = VERSION,
      description = 'Blosc data compressor',
      long_description = """\

Blosc is a high performance compressor optimized for binary data.

""",
      classifiers = [c for c in classifiers.split("\n") if c],
      author = 'Francesc Alted, Valentin Hänel',
      author_email = 'faltet@gmail.com, valentin@haenel.co',
      maintainer = 'Francesc Alted',
      maintainer_email = 'faltet@gmail.com',
      url = 'http://github.com/blosc/python-blosc',
      license = 'https://opensource.org/licenses/BSD-3-Clause',
      platforms = ['any'],
      libraries = clibs,
      ext_modules = [
        Extension( "blosc.blosc_extension",
                   include_dirs=inc_dirs,
                   define_macros=def_macros,
                   sources=sources,
                   library_dirs=lib_dirs,
                   libraries=libs,
                   extra_link_args=LFLAGS,
                   extra_compile_args=CFLAGS ),
        ],
      tests_require=tests_require,
      zip_safe=False,
      packages = ['blosc'],

)
