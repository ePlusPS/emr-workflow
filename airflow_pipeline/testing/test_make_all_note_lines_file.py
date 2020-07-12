import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import make_all_notes_lines_file

class SomeCallableTest(unittest.TestCase):

    #create tests for create_file

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
