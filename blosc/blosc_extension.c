/*********************************************************************
  Blosc - Blocked Suffling and Compression Library

      License: MIT
      Created: September 22, 2010
      Author:  Francesc Alted - faltet@pytables.org

  See LICENSES/BLOSC.txt for details about copyright and rights to use.
**********************************************************************/


#define PY_SSIZE_T_CLEAN   /* allows Py_ssize_t in s# format for parsing arguments */
#include "Python.h"
#include "blosc.h"


static PyObject *BloscError;

static void
blosc_error(int err, char *msg)
{
  PyErr_Format(BloscError, "Error %d %s", err, msg);
}


PyDoc_STRVAR(set_nthreads__doc__,
"set_nthreads(nthreads) -- Initialize a pool of threads for Blosc operation.\n"
             );

static PyObject *
PyBlosc_set_nthreads(PyObject *self, PyObject *args)
{
    int nthreads, old_nthreads;

    if (!PyArg_ParseTuple(args, "i:set_nthreads", &nthreads))
      return NULL;

    old_nthreads = blosc_set_nthreads(nthreads);

    return Py_BuildValue("i", old_nthreads);
}


PyDoc_STRVAR(free_resources__doc__,
"free_resources() -- Free possible memory temporaries and thread resources.\n"
             );

static PyObject *
PyBlosc_free_resources(PyObject *self)
{
    blosc_free_resources();

    return Py_None;
}

static PyObject *
compress_helper(void * input, size_t nbytes,
        size_t typesize, int clevel, int shuffle){

    int cbytes;
    PyObject *output = NULL;

    /* Alloc memory for compression */
    if (!(output = PyBytes_FromStringAndSize(NULL, nbytes+BLOSC_MAX_OVERHEAD)))
      return NULL;

    /* Compress */
    Py_BEGIN_ALLOW_THREADS;
    cbytes = blosc_compress(clevel, shuffle, typesize, nbytes,
                            input, PyBytes_AS_STRING(output),
                            nbytes+BLOSC_MAX_OVERHEAD);
    Py_END_ALLOW_THREADS;
    if (cbytes < 0) {
      blosc_error(cbytes, "while compressing data");
      Py_XDECREF(output);
      return NULL;
    }

    /* Attempt to resize, if it's much smaller, a copy is required. */
    if (_PyBytes_Resize(&output, cbytes) < 0){
        /* the memory exception will have been set, hopefully */
        return NULL;
    }
    return output;
}

PyDoc_STRVAR(compress_ptr__doc__,
"compress_ptr(pointer, len, typesize, clevel, shuffle]) -- Return compressed string.\n"
             );

static PyObject *
PyBlosc_compress_ptr(PyObject *self, PyObject *args)
{
    PyObject * input;
    void * input_ptr;
    size_t nbytes, typesize;
    int clevel, shuffle;

    /* require an address, buffer length, typesize, clevel and shuffle agrs */
    if (!PyArg_ParseTuple(args, "Oiiii:compress", &input, &nbytes,
                          &typesize, &clevel, &shuffle))
      return NULL;
    /*  convert to void pointer safely */
    input_ptr = PyLong_AsVoidPtr(input);
    if (input_ptr == NULL)
      return NULL;
    return compress_helper(input_ptr, nbytes, typesize, clevel, shuffle);
}

PyDoc_STRVAR(compress__doc__,
"compress(string[, typesize, clevel, shuffle]) -- Return compressed string.\n"
             );

static PyObject *
PyBlosc_compress(PyObject *self, PyObject *args)
{
    void *input;
    size_t nbytes, typesize;
    int clevel, shuffle;

    /* require Python string object, typesize, clevel and shuffle agrs */
    if (!PyArg_ParseTuple(args, "s#iii:compress", &input, &nbytes,
                          &typesize, &clevel, &shuffle))
      return NULL;
    return compress_helper(input, nbytes,
            typesize, clevel, shuffle);
}

/*  Read blosc header from input and fetch the uncompressed size into nbytes.
 *  Also makes sure that value of the compressed bytes from the header is the
 *  same as the cbytes provided by the input.
 *
 *  Returns 1 on success and 0 on failure with a Python exception set.
 *
 *  */
static int
get_nbytes(void * input, size_t cbytes, size_t * nbytes)
{
    size_t cbytes2, blocksize;

    /* Get the length of the uncompressed buffer */
    blosc_cbuffer_sizes(input, nbytes, &cbytes2, &blocksize);
    if ((size_t)cbytes != cbytes2) {
      blosc_error((int)cbytes,
                  ": not a Blosc buffer or header info is corrupted");
      return 0;
    }
    return 1;
}

/*  Decompress nbytes from input into output.
 *
 *  Returns 1 on success and 0 on failure with a Python exception set.
 *
 *  */
static int
decompress_helper(void * input, size_t nbytes, void * output)
{
    int err;

    /* Do the decompression */
    Py_BEGIN_ALLOW_THREADS;
    err = blosc_decompress(input, output, nbytes);
    Py_END_ALLOW_THREADS;

    if (err < 0 || err != (int)nbytes) {
      blosc_error(err, "while decompressing data");
      return 0;
    }
    return 1;
}


PyDoc_STRVAR(decompress_ptr__doc__,
"decompress_ptr(string, pointer) -- Decompress string into pointer.\n"
             );

static PyObject *
PyBlosc_decompress_ptr(PyObject *self, PyObject *args)
{
    PyObject * pointer;
    void * input, * output;
    size_t cbytes, nbytes;

    /* require a compressed string and a pointer  */
    if (!PyArg_ParseTuple(args, "s#O:decompress", &input, (Py_ssize_t*)&cbytes, &pointer))
      return NULL;

    /*  convert the int or long Python object to a void * */
    output = PyLong_AsVoidPtr(pointer);
    if (output == NULL)
      return NULL;

    /*  fetch the uncompressed size into nbytes */
    if (!get_nbytes(input, cbytes, &nbytes))
      return NULL;

    /* do decompression */
    if (!decompress_helper(input, nbytes, output))
      return NULL;

    /*  return None, since result was decompressed into output */
    return Py_None;
}

PyDoc_STRVAR(decompress__doc__,
"decompress(string) -- Return decompressed string.\n"
             );

static PyObject *
PyBlosc_decompress(PyObject *self, PyObject *args)
{
    PyObject *result_str;
    void *input, *output;
    size_t nbytes, cbytes;

    if (!PyArg_ParseTuple(args, "s#:decompress", &input, (Py_ssize_t*)&cbytes))
      return NULL;

    /*  fetch the uncompressed size into nbytes */
    if (!get_nbytes(input, cbytes, &nbytes))
      return NULL;

    /* Book memory for the result */
    if (!(result_str = PyBytes_FromStringAndSize(NULL, (Py_ssize_t)nbytes)))
      return NULL;
    output = PyBytes_AS_STRING(result_str);

    /*  do decompression */
    if (!decompress_helper(input, nbytes, output)){
      Py_XDECREF(result_str);
      return NULL;
    }

    return result_str;
}


static PyMethodDef blosc_methods[] =
{
  {"compress", (PyCFunction)PyBlosc_compress,  METH_VARARGS,
   compress__doc__},
  {"compress_ptr", (PyCFunction)PyBlosc_compress_ptr,  METH_VARARGS,
   compress_ptr__doc__},
  {"decompress", (PyCFunction)PyBlosc_decompress, METH_VARARGS,
   decompress__doc__},
  {"decompress_ptr", (PyCFunction)PyBlosc_decompress_ptr, METH_VARARGS,
   decompress_ptr__doc__},
  {"free_resources", (PyCFunction)PyBlosc_free_resources, METH_VARARGS,
   free_resources__doc__},
  {"set_nthreads", (PyCFunction)PyBlosc_set_nthreads, METH_VARARGS,
   set_nthreads__doc__},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION < 3
/* Python 2 module initialization */
PyMODINIT_FUNC
initblosc_extension(void)
{
  PyObject *m;
  m = Py_InitModule("blosc_extension", blosc_methods);
  if (m == NULL)
    return;

  BloscError = PyErr_NewException("blosc_extension.error", NULL, NULL);
  if (BloscError != NULL) {
    Py_INCREF(BloscError);
    PyModule_AddObject(m, "error", BloscError);
  }

  /* Integer macros */
  PyModule_AddIntMacro(m, BLOSC_MAX_BUFFERSIZE);
  PyModule_AddIntMacro(m, BLOSC_MAX_THREADS);
  PyModule_AddIntMacro(m, BLOSC_MAX_TYPESIZE);

  /* String macros */
  PyModule_AddStringMacro(m, BLOSC_VERSION_STRING);
  PyModule_AddStringMacro(m, BLOSC_VERSION_DATE);

}
# else
/* Python 3 module initialization */
static struct PyModuleDef blosc_def = {
  PyModuleDef_HEAD_INIT,
  "blosc_extension",
  NULL,
  -1,
  blosc_methods,
  NULL,
  NULL,
  NULL,
  NULL
};

PyMODINIT_FUNC
PyInit_blosc_extension(void) {
  PyObject *m = PyModule_Create(&blosc_def);

  /* Integer macros */
  PyModule_AddIntMacro(m, BLOSC_MAX_BUFFERSIZE);
  PyModule_AddIntMacro(m, BLOSC_MAX_THREADS);
  PyModule_AddIntMacro(m, BLOSC_MAX_TYPESIZE);

  /* String macros */
  PyModule_AddStringMacro(m, BLOSC_VERSION_STRING);
  PyModule_AddStringMacro(m, BLOSC_VERSION_DATE);

  return m;
}
#endif
