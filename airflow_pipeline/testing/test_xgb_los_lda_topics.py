import sys
sys.path.insert(0,'..')

import unittest
import xgb_los_lda_topics

class SomeCallableTest(unittest.TestCase):

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
