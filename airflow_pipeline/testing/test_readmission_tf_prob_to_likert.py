import sys
sys.path.insert(0,'..')

import unittest
import readmission_tf_prob_to_likert
import pandas as pd

class SomeCallableTest(unittest.TestCase):

    # create tests for make_likert_column
    def test_column_values(self):
        df = pd.DataFrame()
        row1 ={'keras_pred': 0}
        row2 ={'keras_pred':0.2}
        row3 ={'keras_pred':0.35}
        row4 ={'keras_pred':0.83}
        row5 ={'keras_pred':0.67}

        df=df.append(row1, ignore_index=True)
        df=df.append(row2, ignore_index=True)
        df=df.append(row3, ignore_index=True)
        df=df.append(row4, ignore_index=True)
        df=df.append(row5, ignore_index=True)

        likert_values = readmission_tf_prob_to_likert(df)
        expected_values = ['Very Unlikely Readmission','Very Unlikely Readmission','Unlikely Readmission','Very Likely Readmission','Likely Readmission']
        assert(liker_values == expected_values)

if __name__ == '__main__':
    unittest.main()
