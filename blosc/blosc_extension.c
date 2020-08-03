/*********************************************************************
  Blosc - Blocked Shuffling and Compression Library

      License: MIT
      Created: September 22, 2010
      Author:  Francesc Alted - faltet@pytables.org

  See LICENSES/BLOSC.txt for details about copyright and rights to use.
**********************************************************************/

#define PY_SSIZE_T_CLEAN   /* allows Py_ssize_t in s# format for parsing arguments */
#include "Python.h"
#include "blosc.h"

static int RELEASEGIL;
static PyObject *BloscError;

static void
blosc_error(int err, const char *msg)
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


PyDoc_STRVAR(set_blocksize__doc__,
"set_blocksize(blocksize) -- Force the use of a specific blocksize.  \n\
If 0, an automatic blocksize will be used (the default).\n"
             );

static PyObject *
PyBlosc_set_blocksize(PyObject *self, PyObject *args)
{
  Py_ssize_t blocksize;

  if (!PyArg_ParseTuple(args, "n:set_blocksize", &blocksize))
    return NULL;

  blosc_set_blocksize(blocksize);

  Py_RETURN_NONE;
}


PyDoc_STRVAR(get_blocksize__doc__,
"get_blocksize() -- Get the blocksize currently used.\n"
             );

static PyObject *
PyBlosc_get_blocksize(PyObject *self)
{
  int blocksize;

  blocksize = blosc_get_blocksize();

  return Py_BuildValue("i", blocksize);
}


PyDoc_STRVAR(set_releasegil__doc__,
"set_releasegil( gilstate ) -- Whether to release GIL (True) or not (False) during c-blosc calls.\n"
             );

static PyObject *
PyBlosc_set_releasegil(PyObject *self, PyObject *args)
{
  int gilstate, old_gilstate;

  if (!PyArg_ParseTuple(args, "i:gilstate", &gilstate))
    return NULL;

  old_gilstate = RELEASEGIL;
  RELEASEGIL = gilstate;

  return Py_BuildValue("i", old_gilstate);
}


PyDoc_STRVAR(compressor_list__doc__,
"compressor_list() -- Return a list of compressors available in the Blosc build.\n"
             );

static PyObject *
PyBlosc_compressor_list(PyObject *self)
{
  const char *list;

  list = blosc_list_compressors();

  return Py_BuildValue("s", list);
}


PyDoc_STRVAR(code_to_name__doc__,
"code_to_name() -- Return the compressor name of a compressor code.\n"
             );

static PyObject *
PyBlosc_code_to_name(PyObject *self, PyObject *args)
{
  int code;
  const char *name;

  if (!PyArg_ParseTuple(args, "i:code_to_name", &code))
    return NULL;

  if (blosc_compcode_to_compname(code, &name) < 0)
    return NULL;

  return Py_BuildValue("s", name);
}


PyDoc_STRVAR(name_to_code__doc__,
"name_to_code() -- Return the compressor code of a compressor name.\n"
             );

static PyObject *
PyBlosc_name_to_code(PyObject *self, PyObject *args)
{
  int code;
  char *name;

  if (!PyArg_ParseTuple(args, "s:name_to_code", &name))
    return NULL;

  code = blosc_compname_to_compcode(name);
  if (code < 0)
    return NULL;

  return Py_BuildValue("i", code);
}


PyDoc_STRVAR(clib_info__doc__,
"clib_info() -- Return info for compression libraries in the current build.\n"
             );

static PyObject *
PyBlosc_clib_info(PyObject *self, PyObject *args)
{
  char *cname;
  char *clib;
  char *version;
  PyObject *info;

  if (!PyArg_ParseTuple(args, "s:clib_info", &cname))
    return NULL;

  if (blosc_get_complib_info(cname, &clib, &version) < 0)
    return NULL;

  info = Py_BuildValue("(s, s)", clib, version);
  free(clib);
  free(version);
  return info;
}


PyDoc_STRVAR(free_resources__doc__,
"free_resources() -- Free possible memory temporaries and thread resources.\n"
             );

static PyObject *
PyBlosc_free_resources(PyObject *self)
{
  blosc_free_resources();
  Py_RETURN_NONE;
}

PyDoc_STRVAR(init__doc__,
"init() -- Initialize the C-Blosc library environment.\n"
             );

static PyObject *
PyBlosc_init(PyObject *self)
{
  blosc_init();
  Py_RETURN_NONE;
}

PyDoc_STRVAR(destroy__doc__,
"destroy() -- Destroy the C-Blosc library environment.\n"
             );

static PyObject *
PyBlosc_destroy(PyObject *self)
{
  blosc_destroy();
  Py_RETURN_NONE;
}

static PyObject *
compress_helper(void * input, size_t nbytes, size_t typesize,
                int clevel, int shuffle, char *cname){

  int cbytes, blocksize, nthreads;
  PyObject *output;
  char *output_ptr;
  PyThreadState *_save = NULL;


  /* Alloc memory for compression */
  if (!(output = PyBytes_FromStringAndSize(NULL, nbytes+BLOSC_MAX_OVERHEAD)))
    return NULL;

  /* Select compressor */
  if (blosc_set_compressor(cname) < 0) {
    /* The compressor is not available (should never happen here) */
    blosc_error(-1, "compressor not available");
    Py_DECREF(output);
    return NULL;
  }

  /* Compress */
  // This macro probably doesn't require the Python interpreter but let's leave it outside for safety
  output_ptr = PyBytes_AS_STRING(output);

  if( RELEASEGIL )
  {
    // Run with GIL released, tiny overhead penalty from this (although it
    // may be significant for smaller chunks.)

    _save = PyEval_SaveThread();
    blocksize = blosc_get_blocksize();
    // if blocksize==0, blosc_compress_ctx will try to auto-optimize it.
    nthreads = blosc_get_nthreads();
    cbytes = blosc_compress_ctx(clevel, shuffle, typesize, nbytes,
                                input, output_ptr, nbytes+BLOSC_MAX_OVERHEAD,
                                cname, blocksize, nthreads);
     PyEval_RestoreThread(_save);
     _save = NULL;
  }
  else
  { // Hold onto the Python GIL while compressing
    cbytes = blosc_compress(clevel, shuffle, typesize, nbytes,
                            input, output_ptr,
                            nbytes+BLOSC_MAX_OVERHEAD);
  }

  if (cbytes < 0) {
    blosc_error(cbytes, "while compressing data");
    Py_DECREF(output);
    return NULL;
  }


  /* Attempt to resize, if it's much smaller, a copy is required. */
  if (_PyBytes_Resize(&output, cbytes) < 0){
    /* the memory exception will have been set, hopefully */
    Py_DECREF(output);
    return NULL;
  }

  return output;
}

PyDoc_STRVAR(compress_ptr__doc__,
"compress_ptr(pointer, len, typesize[, clevel, shuffle, cname]) -- Return compressed string.\n"
             );

static PyObject *
PyBlosc_compress_ptr(PyObject *self, PyObject *args)
{
  PyObject * input;
  void * input_ptr;
  size_t nbytes, typesize;
  int clevel, shuffle;
  char *cname;

  /* require an address, buffer length, typesize, clevel, shuffle and cname */
  if (!PyArg_ParseTuple(args, "Onniis:compress", &input, &nbytes,
      &typesize, &clevel, &shuffle, &cname))
    return NULL;
  /*  convert to void pointer safely */
  input_ptr = PyLong_AsVoidPtr(input);
  if (input_ptr == NULL)
    return NULL;
  return compress_helper(input_ptr, nbytes, typesize, clevel, shuffle, cname);
}

PyDoc_STRVAR(compress__doc__,
"compress(string, typesize[, clevel, shuffle, cname]) -- Return compressed string.\n"
             );

static PyObject *
PyBlosc_compress(PyObject *self, PyObject *args)
{
  Py_buffer view;
  PyObject *output;
  void *input;
  size_t nbytes, typesize;
  int clevel, shuffle;
  char *cname;
  const char *format;

  /* Accept some kind of input followed by
   * typesize, clevel, shuffle and cname
   * y* :bytes like object EXCLUDING unicode and anything that supports
   * the buffer interface. This is the recommended way to accept binary
   * data in Python 3.
   */
  format = "y*niis:compress";
  if (!PyArg_ParseTuple(args, format , &view,
                        &typesize, &clevel, &shuffle, &cname))
    return NULL;
  nbytes = view.len;
  input = view.buf;
  output = compress_helper(input, nbytes, typesize, clevel, shuffle, cname);
  PyBuffer_Release(&view);
  return output;
}

PyDoc_STRVAR(get_clib__doc__,
"get_clib(string) -- Return the name of the compression library for Blosc buffer.\n"
             );

static PyObject *
PyBlosc_get_clib(PyObject *self, PyObject *args)
{
  void *input;
  size_t cbytes;
  const char *clib;

  /* require Python string object, typesize, clevel and shuffle agrs */
  if (!PyArg_ParseTuple(args, "s#:get_clib", &input, &cbytes))
    return NULL;
  clib = blosc_cbuffer_complib(input);
  return Py_BuildValue("s", clib);
}

PyDoc_STRVAR(get_cbuffer_sizes__doc__,
"get_cbuffer_sizes() -- Return information about a compressed buffer,\
the number of uncompressed and compressed bytes and the blocksize.\n"
            );

static PyObject *
PyBlosc_get_cbuffer_sizes(PyObject *self, PyObject *args)
{
   void *cbuffer;
   size_t auxbytes, nbytes, cbytes, blocksize;

   if (!PyArg_ParseTuple(args, "s#:get_cbuffer_sizes", &cbuffer, &auxbytes))
    return NULL;

   blosc_cbuffer_sizes(cbuffer, &nbytes, &cbytes, &blocksize);

   return Py_BuildValue("nnn", nbytes, cbytes, blocksize);
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
  int err, nthreads;
  PyThreadState *_save = NULL;

  /* Do the decompression */
//  int blosc_decompress_ctx(const void *src, void *dest, size_t destsize,
//                         int numinternalthreads)
  if( RELEASEGIL )
  {

    _save = PyEval_SaveThread();
    nthreads = blosc_get_nthreads();
    err = blosc_decompress_ctx(input, output, nbytes, nthreads);
    PyEval_RestoreThread(_save);
    _save = NULL;
  }
  else
  { // Run while holding the GIL
    err = blosc_decompress(input, output, nbytes);
  }


  if (err < 0) {
    blosc_error(err, "while decompressing data");
    return 0;
  }
  else if (err != (int)nbytes) {
    PyErr_Format(BloscError,
        "expected %d bytes of decompressed data, got %d",
        (int) nbytes,
        err);
    return 0;
  }
  return 1;
}


PyDoc_STRVAR(decompress_ptr__doc__,
"decompress_ptr(bytes_like, pointer) -- Decompress bytes-like into pointer.\n"
             );

static PyObject *
PyBlosc_decompress_ptr(PyObject *self, PyObject *args)
{
  PyObject * pointer;
  Py_buffer input;
  void * output;
  size_t nbytes;

  /* require a compressed string and a pointer  */
  if (!PyArg_ParseTuple(args, "y*O:decompress_ptr", &input, &pointer)){
    PyBuffer_Release(&input);
    return NULL;
  }

  /*  convert the int or long Python object to a void * */
  output = PyLong_AsVoidPtr(pointer);
  if (output == NULL){
    PyBuffer_Release(&input);
    return NULL;
  }

  /*  fetch the uncompressed size into nbytes */
  if (!get_nbytes(input.buf, input.len, &nbytes)){
    PyBuffer_Release(&input);
    return NULL;
  }

  /* do decompression */
  if (!decompress_helper(input.buf, nbytes, output)){
    PyBuffer_Release(&input);
    return NULL;
  }

  /*  Return nbytes as python integer. This is legitimate, because
   *  decompress_helper above has checked that the number of bytes written
   *  was indeed nbytes.
   *  */
  PyBuffer_Release(&input);
  return PyLong_FromSize_t(nbytes);
}

PyDoc_STRVAR(decompress__doc__,
"decompress(string, as_bytearray) -- Return decompressed string.\n\n"
"If as_bytearray is True then the returned data will be a mutable\n"
"bytearray object instead of bytes");

static PyObject *
PyBlosc_decompress(PyObject *self, PyObject *args)
{
  Py_buffer view;
  PyObject *result_str;
  void *input, *output;
  size_t nbytes, cbytes;
  int as_bytearray;

  /* Accept some kind of input
   * y* :bytes like object EXCLUDING unicode and anything that supports
   * the buffer interface. This is the recommended way to accept binary
   * data in Python 3.
   */
  if (!PyArg_ParseTuple(args, "y*p:decompress", &view, &as_bytearray))
    return NULL;

  cbytes = view.len;
  input = view.buf;
  /*  fetch the uncompressed size into nbytes */
  if (!get_nbytes(input, cbytes, &nbytes)){
    PyBuffer_Release(&view);
    return NULL;
  }

#define branch(from_string_and_size, as_string)                               \
  /* Book memory for the result */                                            \
    if (!(result_str = from_string_and_size(NULL, (Py_ssize_t)nbytes))){      \
      PyBuffer_Release(&view);                                                \
      return NULL;                                                            \
    }                                                                         \
                                                                              \
    output = as_string(result_str);                                           \
    (void)NULL

  if (as_bytearray) {
    branch(PyByteArray_FromStringAndSize, PyByteArray_AS_STRING);
  }
  else {
    branch(PyBytes_FromStringAndSize, PyBytes_AS_STRING);
  }

#undef branch

  /*  do decompression */
  if (!decompress_helper(input, nbytes, output)){
    Py_XDECREF(result_str);
    PyBuffer_Release(&view);
    return NULL;
  }

  PyBuffer_Release(&view);
  return result_str;
}


PyDoc_STRVAR(cbuffer_validate__doc__,
"cbuffer_validate(bytesobj) -- Check if compressed data is safe.\n\n"
"Checks that it is safe to attempt decompression of compressed data.\n"
"This does not guarantee that decompression will be successful,\n"
"only that it is safe to attempt decompression.");

static PyObject *
PyBlosc_cbuffer_validate(PyObject *self, PyObject *args)
{
  Py_buffer view;
  void *input;
  size_t nbytes, cbytes;
  int result;

  /* Accept some kind of input
   * y* :bytes like object EXCLUDING unicode and anything that supports
   * the buffer interface. This is the recommended way to accept binary
   * data in Python 3.
   */
  if (!PyArg_ParseTuple(args, "y*:cbuffer_validate", &view))
    return NULL;
  cbytes = view.len;
  input = view.buf;
  result = blosc_cbuffer_validate(input, cbytes, &nbytes);
  if (result == 0) {
    Py_RETURN_TRUE;
  }else{
    Py_RETURN_FALSE;
  }
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
  {"set_blocksize", (PyCFunction)PyBlosc_set_blocksize, METH_VARARGS,
   set_blocksize__doc__},
  {"get_blocksize", (PyCFunction)PyBlosc_get_blocksize, METH_VARARGS,
   get_blocksize__doc__},
  {"set_releasegil", (PyCFunction)PyBlosc_set_releasegil, METH_VARARGS,
   set_releasegil__doc__},
  {"compressor_list", (PyCFunction)PyBlosc_compressor_list, METH_VARARGS,
   compressor_list__doc__},
  {"code_to_name", (PyCFunction)PyBlosc_code_to_name, METH_VARARGS,
   code_to_name__doc__},
  {"name_to_code", (PyCFunction)PyBlosc_name_to_code, METH_VARARGS,
   name_to_code__doc__},
  {"clib_info", (PyCFunction)PyBlosc_clib_info, METH_VARARGS,
   clib_info__doc__},
  {"get_clib", (PyCFunction)PyBlosc_get_clib, METH_VARARGS,
   get_clib__doc__},
  {"get_cbuffer_sizes", (PyCFunction)PyBlosc_get_cbuffer_sizes, METH_VARARGS,
   get_cbuffer_sizes__doc__},
  {"cbuffer_validate", (PyCFunction)PyBlosc_cbuffer_validate, METH_VARARGS,
   cbuffer_validate__doc__},
  {"init", (PyCFunction)PyBlosc_init, METH_VARARGS,
   init__doc__},
  {"destroy", (PyCFunction)PyBlosc_destroy, METH_VARARGS,
   destroy__doc__},
    {NULL, NULL, 0, NULL},
};


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


  BloscError = PyErr_NewException("blosc_extension.error", NULL, NULL);
  if (BloscError != NULL) {
    Py_INCREF(BloscError);
    PyModule_AddObject(m, "error", BloscError);
  }

  /* Integer macros */
  PyModule_AddIntMacro(m, BLOSC_MAX_BUFFERSIZE);
  PyModule_AddIntMacro(m, BLOSC_MAX_THREADS);
  PyModule_AddIntMacro(m, BLOSC_MAX_TYPESIZE);
  PyModule_AddIntMacro(m, BLOSC_NOSHUFFLE);
  PyModule_AddIntMacro(m, BLOSC_SHUFFLE);
  PyModule_AddIntMacro(m, BLOSC_BITSHUFFLE);

  /* String macros */
  PyModule_AddStringMacro(m, BLOSC_VERSION_STRING);
  PyModule_AddStringMacro(m, BLOSC_VERSION_DATE);

  return m;
}


