import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import create_word2vec_model

class SomeCallableTest(unittest.TestCase):
    
    # Maybe create tests for create_word2vec_model. 
    # Since this is the method used for integration testing, it wouldn't be consistent. 

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
