import sys
sys.path.insert(0,'..')

import unittest
import xgb_los_lda_topics
import pandas as pd

class SomeCallableTest(unittest.TestCase):

    #tests for make_one_hot
    def test_make_one_hot_standard(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'lda_ngrams':['blood_pressure_greater_than_100','fractured_rib_and_broken_femur']}
        row2 = {'admission_id':2, 'lda_ngrams':[]}
        row3 = {'admission_id':3, 'lda_ngrams':['fractured_rib_and_broken_femur']}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)
        
        one_hot = xgb_los_lda_topics.make_one_hot(df)

        all_valid = True
        expected_blood_pressure_column = [1,0,0]
        expected_fractured_rib_column = [1,0,1]
        
        if one_hot['blood_pressure_greater_than_100'].to_list() != expected_blood_pressure_column:
            all_valid = False
        if one_hot['fractured_rib_and_broken_femur'].to_list() != expected_fractured_rib_column:
            all_valid = False

        assert(all_valid)

        
    #tests for train_xgb_model
    def test_train_xgb_model_not_null(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'lda_ngrams':['blood_pressure_greater_than_100','fractured_rib_and_broken_femur'], 'los': 1}
        row2 = {'admission_id':2, 'lda_ngrams':[], 'los': 5}
        row3 = {'admission_id':3, 'lda_ngrams':['fractured_rib_and_broken_femur'], 'los': 10}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        one_hot = pd.DataFrame()
        oh_row1 = {'blood_pressure_greater_than_100': 1, 'fractured_rib_and_broken_femur': 1}
        oh_row2 = {'blood_pressure_greater_than_100': 0, 'fractured_rib_and_broken_femur': 0}
        oh_row3 = {'blood_pressure_greater_than_100': 0, 'fractured_rib_and_broken_femur': 1}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)
        one_hot = one_hot.append(oh_row3, ignore_index=True)
        
        xgb_model = xgb_los_lda_topics.train_xgb_model(df, one_hot)

        assert(xgb_model != None)

    #tests for add_predictions_column
    def test_add_predictions_column_no_null_entries(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'lda_ngrams':['blood_pressure_greater_than_100','fractured_rib_and_broken_femur'], 'los': 1}
        row2 = {'admission_id':2, 'lda_ngrams':[], 'los': 5}
        row3 = {'admission_id':3, 'lda_ngrams':['fractured_rib_and_broken_femur'], 'los': 10}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        one_hot = pd.DataFrame()
        oh_row1 = {'blood_pressure_greater_than_100': 1, 'fractured_rib_and_broken_femur': 1}
        oh_row2 = {'blood_pressure_greater_than_100': 0, 'fractured_rib_and_broken_femur': 0}
        oh_row3 = {'blood_pressure_greater_than_100': 0, 'fractured_rib_and_broken_femur': 1}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)
        one_hot = one_hot.append(oh_row3, ignore_index=True)
        
        xgb_model = xgb_los_lda_topics.train_xgb_model(df, one_hot)

        updated_df = xgb_los_lda_topics.add_predictions_column(df, xgb_model, one_hot)

        null_count = 0
        for i, row in updated_df.iterrows():
            if row['xgb_lda_pred'] == None:
                null_count += 1
        assert(null_count == 0)

    #tests for make_top_n_features
    def test_make_top_n_features_check_num_features(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'lda_ngrams':['blood_pressure_greater_than_100','fractured_rib_and_broken_femur'], 'los': 1}
        row2 = {'admission_id':2, 'lda_ngrams':['headache', 'nausea'], 'los': 3}
        row3 = {'admission_id':3, 'lda_ngrams':['fractured_rib_and_broken_femur'], 'los': 10}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True) 
        df = df.append(row3, ignore_index=True)
        one_hot = pd.DataFrame()
        oh_row1 = {'blood_pressure_greater_than_100': 1, 'fractured_rib_and_broken_femur': 1, 'headache': 0, 'nausea': 0}
        oh_row2 = {'blood_pressure_greater_than_100': 0, 'fractured_rib_and_broken_femur': 0, 'headache': 1, 'nausea': 1}
        oh_row3 = {'blood_pressure_greater_than_100': 0, 'fractured_rib_and_broken_femur': 1, 'headache': 0, 'nausea': 0}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)
        one_hot = one_hot.append(oh_row3, ignore_index=True)
        xgb_model = xgb_los_lda_topics.train_xgb_model(df, one_hot)

        top_2_df = xgb_los_lda_topics.make_top_n_features(xgb_model, one_hot, 2)
        assert(len(top_2_df.columns) <= 2)

if __name__ == '__main__':
    unittest.main()
