import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import fe_from_structured_readmit_los

class SomeCallableTest(unittest.TestCase):

    # tests for add_los_age_and_binary_deathtime_columns 
    
    # tests for add_readmission_column
    
    #may be worth breaking out readmission flag logic to a function per-row. Easier testing that way.

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
