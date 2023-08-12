import unittest

import numpy as np

from sateda.core.time import Time

class TestTime(unittest.TestCase):
    def setUp(self) -> None:
        self.time = Time.from_components(2007,1,1,0,0,0,0)
    def test_something(self):
        self.assertTrue(self.time.time == np.datetime64("2007-01-01T00:00:00.000000000"))
        self.assertTrue(self.time.to_utc().time == np.datetime64("2006-12-31T23:59:46.0000000"))
        self.assertTrue(self.time.to_tt().time == np.datetime64("2007-01-01T00:00:51.1840000"))
        self.assertTrue(self.time.to_tai().time == np.datetime64("2007-01-01T00:00:19.0000000"))



if __name__ == '__main__':
    unittest.main()
