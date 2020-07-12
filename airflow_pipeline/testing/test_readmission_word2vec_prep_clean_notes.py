import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import readmission_word2vec_prep_clean_notes

class SomeCallableTest(unittest.TestCase):
    
    # create tests for combine_and_clean

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
