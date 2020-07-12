import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import readmission_classifier_train_and_predict

class SomeCallableTest(unittest.TestCase):

    # create tests for create_dataset, train_classifier, and make_probability_column
    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
