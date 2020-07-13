import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import ner_prep_clean_notes

class SomeCallableTest(unittest.TestCase):

    #create tests for clean_ner_notes


    #will likely create more helper functions in this script for more modular testing and maintainability

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
