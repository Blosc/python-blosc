===============================================
 Compiling C files with blosc wheels on Linux
===============================================

- The main requirement for compiling C files on Windows is having installed a Microsoft compiler. You can either install Visual Studio with the Visual C++ components or the Build Tools for Visual Studio. The last package only contains the command-line toolset, compilers and libraries you need to build C programs. If you do not have none of them yet, they are easy to install following the instructions on https://visualstudio.microsoft.com/es/downloads/.

- Once installed MSVC, the first step is to open the Visual Studio directory, which typical installation location uses to be  C:\\Program files (x86)\\Microsoft Visual Studio. Then, to set up the build architecture environment you can open a command prompt window in the VC\\Auxiliary\\Build subdirectory and execute "vcvarsall.bat x64" if your achitecture is 64 bits or "vcvarsall.bat x86" if it is 32 bits.

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

- The output shows the path of blosc.lib, but the directory lib is not the one where all the wheel files are stored. Then, you can save the path of the directory before lib in a new variable. In this case it would be:

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

