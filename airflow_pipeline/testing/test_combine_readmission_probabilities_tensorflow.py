import sys
sys.path.insert(0,'..')

import unittest
import pandas as pd
import combine_readmission_probabilities_tensorflow

class SomeCallableTest(unittest.TestCase):

    # tests for create_model
    def test_create_model_not_null(self):
        df = pd.DataFrame()
        row1 = {'nausea':0, 'headache':1, 'bp_higher_than_100':0, 'broken_femur':1}
        row2 = {'nausea':1, 'headache':0, 'bp_higher_than_100':0, 'broken_femur':1}
        row3 = {'nausea':1, 'headache':1, 'bp_higher_than_100':1, 'broken_femur':1}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        label_df = pd.DataFrame()
        label_df['readmission'] = [1, 0, 1]
        labels = label_df['readmission']

        model = combine_readmission_probabilities_tensorflow.create_model(df, labels)

        assert(model != None)

    # tests for predict_with_model
    def test_predict_with_model_no_null_values(self):
        df = pd.DataFrame()
        row1 = {'nausea':0, 'headache':1, 'bp_higher_than_100':0, 'broken_femur':1}
        row2 = {'nausea':1, 'headache':0, 'bp_higher_than_100':0, 'broken_femur':1}
        row3 = {'nausea':1, 'headache':1, 'bp_higher_than_100':1, 'broken_femur':1}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        label_df = pd.DataFrame()
        label_df['readmission'] = [1,0,1]
        labels = label_df['readmission']

        model = combine_readmission_probabilities_tensorflow.create_model(df, labels)

        predictions = combine_readmission_probabilities_tensorflow.predict_with_model(df, model)

        null_count = 0
        for prediction in predictions:
            if prediction == None:
                null_count += 1

        assert(null_count == 0)

    def test_predict_with_model_values_between_0_and_1(self):
        df = pd.DataFrame()
        row1 = {'nausea':0, 'headache':1, 'bp_higher_than_100':0, 'broken_femur':1}
        row2 = {'nausea':1, 'headache':0, 'bp_higher_than_100':0, 'broken_femur':1}
        row3 = {'nausea':1, 'headache':1, 'bp_higher_than_100':1, 'broken_femur':1}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        label_df = pd.DataFrame()
        label_df['readmission'] = [1,0,1]
        labels = label_df['readmission']

        model = combine_readmission_probabilities_tensorflow.create_model(df, labels)

        predictions = combine_readmission_probabilities_tensorflow.predict_with_model(df, model)

        out_of_range_count = 0
        for prediction in predictions:
            if prediction <0 or prediction > 1:
                out_of_range_count += 1

        assert(out_of_range_count == 0)


if __name__ == '__main__':
    unittest.main()
