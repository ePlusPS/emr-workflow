import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import create_report_summary

class SomeCallableTest(unittest.TestCase):
    
    # tests for make_patient_summary 
    # tests for make_hospital_summary

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
