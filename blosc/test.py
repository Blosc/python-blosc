import unittest
import blosc

class TestCodec(unittest.TestCase):

    def test_basic_codec(self):
        s = '0123456789'
        c = blosc.compress(s, typesize=1)
        d = blosc.decompress(c)
        self.assertEqual(s, d)

    def test_compress_exceptions(self):
        s = '0123456789'

        self.assertRaises(ValueError, blosc.compress, s, typesize=1, clevel=-1)
        self.assertRaises(ValueError, blosc.compress, s, typesize=1, clevel=10)

        self.assertRaises(ValueError, blosc.compress, 1.0, 1)
        self.assertRaises(ValueError, blosc.compress, ['abc'], 1)

        self.assertRaises(ValueError, blosc.compress,
                'a' * (blosc.BLOSC_MAX_BUFFERSIZE+1), typesize=1)


if __name__ == '__main__':
        unittest.main()
