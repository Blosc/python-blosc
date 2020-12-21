=====================================================
 Compiling C files with blosc wheels on Windows
=====================================================

- The main requirement for compiling C files on Windows is having installed a Microsoft compiler. You can either install Visual Studio with the Visual C++ components or the Build Tools for Visual Studio. The last package only contains the command-line toolset, compilers and libraries you need to build C programs. If you do not have none of them yet, they are easy to install following the instructions on https://visualstudio.microsoft.com/es/downloads/.

- Blosc libraries are also necessary, so if you do not have them installed you just have to open a command prompt window and execute:

.. code-block:: console

    > pip install blosc
    Collecting blosc==1.9.3.dev0
      Using cached blosc-1.9.3.dev0-cp37-cp37m-win_amd64.whl (1.5 MB)
    Installing collected packages: blosc
    Successfully installed blosc-1.9.3.dev0

- Once installed MSVC and blosc, the first step is to open the Visual Studio directory, which typical installation location uses to be  C:\\Program files (x86)\\Microsoft Visual Studio. Then, to set up the build architecture environment you can open a command prompt window in the VC\\Auxiliary\\Build subdirectory and execute "vcvarsall.bat x64" if your achitecture is 64 bits or "vcvarsall.bat x86" if it is 32 bits.

- Now, in order to verify that the MSVC command line is set up correctly enter ``cl`` in the command prompt window and verify that the output looks something like this:

.. code-block:: console

    > cl
    Microsoft (R) C/C++ Optimizing Compiler Version 19.00.24245 for x64
    Copyright (C) Microsoft Corporation.  All rights reserved.

    usage: cl [ option... ] filename... [ /link linkoption... ]

- For the next steps you will need to know the path where blosc wheel has installed its files:

.. code-block:: console

    > dir /s c:\blosc.lib
     Volume in drive C is OS
     Volume Serial Number is 7A21-A5D5

     Directory of c:\Users\user\miniconda3\Lib

    14/12/2020  09:56             7.022 blosc.lib
                   1 File(s)          7.022 bytes

         Total list files:
                   1 File(s)          7.022 bytes
                   0 dirs  38.981.902.336 free bytes

- The output shows the path of blosc.lib, but the directory lib is not the one where all the wheel files are stored. You can save the path of the lib parent directory in a new variable:

.. code-block:: console

    > set WHEEL_DIR=c:\Users\user\miniconda3\


- It is important to copy the library `blosc.dll` to C:\\Windows\\System32 directory, so it can be found by the processor when it is necessary.

- To compile C files using blosc you only need to open a comand prompt window in the directory which contains the files and enter the command:

.. code-block:: console

    > cl <file_name>.c <path_of_blosc.lib> /Ox /Fe<file_name>.exe /I<path_of_blosc.h> /MT /link/NODEFAULTLIB:MSVCRT

- In the case of blosc example "simple.c":

.. code-block:: console

    > cl simple.c %WHEEL_DIR%\lib\blosc.lib /Ox /Fesimple.exe /I%WHEEL_DIR%\include /MT /link/NODEFAULTLIB:MSVCRT

    Microsoft (R) C/C++ Optimizing Compiler Version 19.10.25017 for x86
    Copyright (C) Microsoft Corporation.  All rights reserved.

    simple.c
    Microsoft (R) Incremental Linker Version 14.10.25017.0
    Copyright (C) Microsoft Corporation.  All rights reserved.

    /out:simple.exe
    simple.obj
    /NODEFAULTLIB:MSVCRT
    .\miniconda3\lib\blosc.lib


- To run your program, enter its name (in the case of simple.c it would be "simple") at a command prompt window:

.. code-block:: console

    > simple
    Blosc version info: 1.20.1 ($Date:: 2020-09-08 #$)
    Compression: 4000000 -> 37816 (105.8x)
    Decompression succesful!
    Succesful roundtrip!


===============================================
 Compiling C files with blosc wheels on Linux
===============================================

- The main requirement for compiling C files on Linux is having installed GCC. If you do not have it yet, you can install it typing the following commands (on Ubuntu or Debian):

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get install build-essential manpages-dev

- To make sure that the GCC compiler is installed:

.. code-block:: console

    $ gcc --version
    gcc (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0
    Copyright (C) 2017 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

- Blosc libraries are also necessary, so if you do not have them installed you just have to execute:

.. code-block:: console

    $ pip install blosc
    Collecting blosc==1.9.3.dev0
      Using cached blosc-1.9.3.dev0-cp37-cp37m-manylinux2010_x86_64.whl (2.2 MB)
    Installing collected packages: blosc
    Successfully installed blosc-1.9.3.dev0

- For the next steps you will need to know the path where blosc wheel has installed its files:

.. code-block:: console

    $ find / -name libblosc.so 2>/dev/null
    /home/soscar/miniconda3/lib/libblosc.so

- The output shows the path of libblosc.so, but the directory lib is not the one where all the wheel files are stored. You can save the path of the lib parent directory in a new variable:

.. code-block:: console

    $ WHEEL_DIR=/home/soscar/miniconda3/

- Once installed GCC and blosc, to compile C files using blosc you only need to enter the commands:

.. code-block:: console

    $ export LD_LIBRARY_PATH=<path_of_libblosc.so>
    $ gcc <file_name>.c -I<path_of_blosc.h> -o <file_name> -L<path_of_libblosc.so> -lblosc

- In the case of blosc example "many_compressors.c":

.. code-block:: console

    $ export LD_LIBRARY_PATH=$WHEEL_DIR/lib/
    $ gcc many_compressors.c -I$WHEEL_DIR/include/ -o many_compressors -L$WHEEL_DIR/lib/ -lblosc

- To run your program, enter "./<filename>". In the case of many_compressors.c it would be "./many_compressors":

.. code-block:: console

    $ ./many_compressors
    Blosc version info: 1.20.1 ($Date:: 2020-09-08 #$)
    Using 4 threads (previously using 1)
    Using blosclz compressor
    Compression: 4000000 -> 37816 (105.8x)
    Succesful roundtrip!
    Using lz4 compressor
    Compression: 4000000 -> 37938 (105.4x)
    Succesful roundtrip!
    Using lz4hc compressor
    Compression: 4000000 -> 27165 (147.2x)
    Succesful roundtrip!

