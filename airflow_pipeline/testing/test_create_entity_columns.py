import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import create_entity_columns

class SomeCallableTest(unittest.TestCase):

    # tests for extract_entities 
    # tests for get_columns_from_notes

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
