from __future__ import division
import sys
import unittest
import ctypes
import numpy
import blosc


py3 = sys.version_info[0] == 3


class TestCodec(unittest.TestCase):

    def test_basic_codec(self):
        s = b'0123456789'
        c = blosc.compress(s, typesize=1)
        d = blosc.decompress(c)
        self.assertEqual(s, d)

    def test_set_nthreads_exceptions(self):
        self.assertRaises(ValueError, blosc.set_nthreads,
                blosc.BLOSC_MAX_THREADS +1)

    def test_compress_exceptions(self):
        rs = '0123456789'
        s = b'0123456789'

        if py3:
            self.assertRaises(ValueError, blosc.compress, rs, typesize=1)
        self.assertRaises(ValueError, blosc.compress, s, typesize=1, clevel=-1)
        self.assertRaises(ValueError, blosc.compress, s, typesize=1, clevel=10)

        self.assertRaises(ValueError, blosc.compress, 1.0, 1)
        self.assertRaises(ValueError, blosc.compress, ['abc'], 1)

        self.assertRaises(ValueError, blosc.compress,
                'a' * (blosc.BLOSC_MAX_BUFFERSIZE+1), typesize=1)

    def test_compress_ptr_exceptions(self):
        # Make sure we do have a valid address, to reduce the chance of a
        # segfault if we do actually start compressing because the exceptions
        # aren't raised.
        typesize, items = 8, 8
        data = [float(i) for i in range(items)]
        Array = ctypes.c_double * items
        array = Array(*data)
        address = ctypes.addressof(array)

        self.assertRaises(ValueError, blosc.compress_ptr, address, items,
                typesize=typesize, clevel=-1)
        self.assertRaises(ValueError, blosc.compress_ptr, address, items,
                typesize=typesize, clevel=10)


        self.assertRaises(TypeError, blosc.compress_ptr, 1.0, -1,
                typesize=typesize)
        self.assertRaises(TypeError, blosc.compress_ptr, 1.0, items,
                typesize=typesize)
        self.assertRaises(TypeError, blosc.compress_ptr, ['abc'], items,
                typesize=typesize)

        self.assertRaises(ValueError, blosc.compress_ptr, address,
                blosc.BLOSC_MAX_BUFFERSIZE+1, typesize=typesize)

    def test_decompress_exceptions(self):
        self.assertRaises(ValueError, blosc.decompress, 1.0)
        self.assertRaises(ValueError, blosc.decompress, ['abc'])

    def test_decompress_ptr_exceptions(self):
        # make sure we do have a valid address
        typesize, items = 8, 8
        data = [float(i) for i in range(items)]
        Array = ctypes.c_double * items
        in_array = Array(*data)
        c = blosc.compress_ptr(ctypes.addressof(in_array), items, typesize)
        out_array = ctypes.create_string_buffer(items*typesize)

        self.assertRaises(ValueError, blosc.decompress_ptr, 1.0,
                ctypes.addressof(out_array))
        self.assertRaises(ValueError, blosc.decompress_ptr, ['abc'],
                ctypes.addressof(out_array))

        self.assertRaises(TypeError, blosc.decompress_ptr, c,
                1.0)
        self.assertRaises(TypeError, blosc.decompress_ptr, c,
                ['abc'])

    def test_pack_array_exceptions(self):
        self.assertRaises(ValueError, blosc.pack_array, 'abc')
        self.assertRaises(ValueError, blosc.pack_array, 1.0)

        items = (blosc.BLOSC_MAX_BUFFERSIZE / 8) +1
        one = numpy.ones(1)
        # use stride trick to make an array that looks like a huge one
        ones = numpy.lib.stride_tricks.as_strided(one, shape=(1,items),
                strides=(8,0))[0]
        # if the value error is not raised, may run out of memory, depending on
        # the machine.
        self.assertRaises(ValueError, blosc.pack_array, ones)

    def test_unpack_array_exceptions(self):
        self.assertRaises(ValueError, blosc.unpack_array, 1.0)


def run():
    import blosc.toplevel
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCodec)
    # If in the future we split this test file in several, the auto-discover
    # might be interesting

    # suite = unittest.TestLoader().discover(start_dir='.', pattern='test*.py')
    suite.addTests(unittest.TestLoader().loadTestsFromModule(blosc.toplevel))
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    run()
