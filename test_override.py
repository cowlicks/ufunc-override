import unittest

import ufunc_override as np

# A class to use for testing overrides.
class DummyClass(object):
    def __init__(self):
        pass
    def dummy_func(*args, **kwargs):
        return 42
    __array_priority__ = 12
    __ufunc_override__ = {np.add.__name__:dummy_func}

class TestOverride(unittest.TestCase):
    def test_override(self):
        a = np.array([1])
        b = DummyClass()
        self.assertEqual(a + b, 42)

if __name__ == '__main__':
    unittest.main()
