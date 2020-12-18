===============================================
 Compiling C files with blosc wheels on Linux
===============================================

- The main requirement for compiling C files on Linux is having installed GCC. If you do not have it yet, you can install it typing the following apt-get commands:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get install build-essential manpages-dev

- To validate that the GCC compiler is successfully installed:

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

- The output shows the path of libblosc.so, but the directory lib is not the one where all the wheel files are stored. Then, you can save the path of the directory before lib in a new variable. In this case it would be:

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

