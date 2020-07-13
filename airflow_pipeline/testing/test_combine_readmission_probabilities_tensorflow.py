import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import combine_readmission_probabilities_tensorflow

class SomeCallableTest(unittest.TestCase):

    # tests for create_model 
    # tests for predict_with_model

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
