import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
#import somecallable
import first_table_from_api
class SomeCallableTest(unittest.TestCase):
    
    # tests for get_all_notes
    
    # tests for get_admissions
    
    # tests for get_icd_codes
    
    # tests for get_patients
    
    # tests for combine_notes_and_admissions_and_codes
    
    #example tests
    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
