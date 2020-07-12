import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
#import somecallable
import first_table_from_api
class SomeCallableTest(unittest.TestCase):
    
    # write tests for each api function: get_all_notes, get_admissions, get_icd_codes, get_patients
    # write tests for combine_notes_and_admissions_and_codes

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
