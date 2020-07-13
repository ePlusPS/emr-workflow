import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import xgb_readmission_feature_entities

class SomeCallableTest(unittest.TestCase):

    # tests for make_one_hot
    
    # tests for train_xgb_model
    
    # tests for add_predictions_column
    
    # tests for make_top_n_features


    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
