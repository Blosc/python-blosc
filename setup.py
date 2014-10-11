# -*- coding: utf-8 -*-
########################################################################
#
#       License: MIT
#       Created: September 22, 2010
#       Author:  Francesc Alted - faltet@gmail.com
#
########################################################################

import sys, os

from distutils.core import Extension
from distutils.core import setup
import glob

########### Check versions ##########

def exit_with_error(message):
    print('ERROR: %s' % message)
    sys.exit(1)

# Check for Python
if sys.version_info[0] == 2:
    if sys.version_info[1] < 6:
        exit_with_error("You need Python 2.6 or greater to install blosc!")
elif sys.version_info[0] == 3:
    if sys.version_info[1] < 1:
        exit_with_error("You need Python 3.1 or greater to install blosc!")
else:
    exit_with_error("You need Python 2.6/3.1 or greater to install blosc!")

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

# Add -msse2 flag for optimizing shuffle in Blosc
if os.name == 'posix':
    CFLAGS.append("-msse2")

# Blosc sources and headers
sources = ["blosc/blosc_extension.c"]
inc_dirs = []
lib_dirs = []
libs = []
def_macros = []
if BLOSC_DIR != '':
    # Using the Blosc library
    lib_dirs += [os.path.join(BLOSC_DIR, 'lib')]
    inc_dirs += [os.path.join(BLOSC_DIR, 'include')]
    libs += ['blosc']
else:
    # Compiling everything from sources
    # Blosc + BloscLZ sources
    sources += glob.glob('c-blosc/blosc/*.c')
    # LZ4 sources
    sources += glob.glob('c-blosc/internal-complibs/lz4*/*.c')
    # Snappy sources
    sources += glob.glob('c-blosc/internal-complibs/snappy*/*.cc')
    # Zlib sources
    sources += glob.glob('c-blosc/internal-complibs/zlib*/*.c')
    # Finally, add all the include dirs...
    inc_dirs += [os.path.join('c-blosc', 'blosc')]
    inc_dirs += glob.glob('c-blosc/internal-complibs/*')
    # ...and the macros for all the compressors supported
    def_macros += [('HAVE_LZ4', 1), ('HAVE_SNAPPY', 1), ('HAVE_ZLIB', 1)]


classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python
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
      classifiers = filter(None, classifiers.split("\n")),
      author = 'Francesc Alted, Valentin Hänel',
      author_email = 'faltet@gmail.com, valentin@haenel.co',
      maintainer = 'Francesc Alted, Valentin Hänel',
      maintainer_email = 'faltet@gmail.com, valentin@haenel.co',
      url = 'http://github.com/blosc/python-blosc',
      license = 'http://www.opensource.org/licenses/mit-license.php',
      platforms = ['any'],
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
      packages = ['blosc'],

)
