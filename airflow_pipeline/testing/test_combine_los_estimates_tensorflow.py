import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import combine_los_estimates_tensorflow

class SomeCallableTest(unittest.TestCase):

    # create tests for create_model and predict_with_model

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
