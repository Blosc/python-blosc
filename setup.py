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
    elif arg.find('--cflags=') == 0:
        CFLAGS = arg.split('=')[1].split()
        sys.argv.remove(arg)

# Add -msse2 flag for optimizing shuffle in Blosc
if os.name == 'posix':
    CFLAGS.append("-msse2")

lib_dirs = []
libs = []
# Add some macros here for debugging purposes, if needed
def_macros = []

# c-blosc sources and header
if BLOSC_DIR == '':
    c_blosc_source_dir = os.path.join('c-blosc', 'blosc')
    c_blosc_sources = [os.path.join(c_blosc_source_dir, source)
                       for source in ('blosc.c', 'blosclz.c', 'shuffle.c')]
    c_blosc_headers = [os.path.join(c_blosc_source_dir, header)
                       for header in ('blosc.h', 'blosclz.h', 'shuffle.h')]
    inc_dirs = [c_blosc_source_dir]
else:
    lib_dirs = [os.path.join(BLOSC_DIR, 'lib')]
    libs = ['blosc']
    inc_dirs = [os.path.join(BLOSC_DIR, 'include')]
    c_blosc_sources = []
    c_blosc_headers = ['blosc.h']


classifiers = """\
Development Status :: 5 - Production
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
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
      author_email = 'faltet@gmail.com',
      maintainer = 'Francesc Alted',
      maintainer_email = 'faltet@gmail.com',
      url = 'http://github.com/FrancescAlted/python-blosc',
      license = 'http://www.opensource.org/licenses/mit-license.php',
      # It is better to upload manually to PyPI
      #download_url = 'http://github.com/downloads/FrancescAlted/python-blosc/python-blosc-%s.tar.gz' % (VERSION,),
      platforms = ['any'],
      ext_modules = [
        Extension( "blosc.blosc_extension",
                   include_dirs=inc_dirs,
                   define_macros=def_macros,
                   sources = ["blosc/blosc_extension.c"] + c_blosc_sources,
                   depends = c_blosc_headers,
                   library_dirs=lib_dirs,
                   libraries=libs,
                   extra_link_args=LFLAGS,
                   extra_compile_args=CFLAGS ),
        ],
      packages = ['blosc'],

)
