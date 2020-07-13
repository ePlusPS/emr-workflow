import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import fe_from_infection_keywords

class SomeCallableTest(unittest.TestCase):

    # tests for find_infection_similar_terms

    # tests for add_found_words_column

    # tests for one_hot_encode_found_key_terms

    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
