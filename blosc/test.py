import unittest
import blosc

class TestCodec(unittest.TestCase):

    def test_basic_codec(self):
        s = '0123456789'
        c = blosc.compress(s, typesize=1)
        d = blosc.decompress(c)
        self.assertEqual(s, d)

