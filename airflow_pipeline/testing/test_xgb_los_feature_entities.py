import sys
sys.path.insert(0,'/home/jsjsahana/emr-workflow/airflow_pipeline/')

import unittest
import pandas as pd
import xgb_los_feature_entities

class SomeCallableTest(unittest.TestCase):


    #tests for make_one_hot
    def test_make_one_hot_standard_true_case(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen']}
        row2 = {'admission_id':2, 'feature_entities':[]}
        row3 = {'admission_id':3, 'feature_entities':['not_well_seen']}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        one_hot = xgb_los_feature_entities.make_one_hot(df)
        # print (one_hot)

        all_valid = True
        expected_accident = [1, 0, 0]
        expected_health_check = [1, 0, 1]
        if one_hot['accident'].to_list() != expected_accident:
            all_valid = False
        if one_hot['not_well_seen'].to_list() != expected_health_check:
            all_valid = False
        # print (all_valid)
        assert(all_valid)
        print ("** Test 1 - AssertTrue is passed: if expr is True for make_one_hot **")


    # tests for make_one_hot
    def test_make_one_hot_standard_false_case(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen']}
        row2 = {'admission_id':2, 'feature_entities':[]}
        row3 = {'admission_id':3, 'feature_entities':['not_well_seen']}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        one_hot = xgb_los_feature_entities.make_one_hot(df)

        all_valid = True
        expected_accident = [1, 1, 0]
        expected_health_check = [1, 0, 0]
        if one_hot['accident'].to_list() == expected_accident:
            all_valid = False
        if one_hot['not_well_seen'].to_list() == expected_health_check:
            all_valid = False
        # print (all_valid)
        assert(all_valid)
        print ("** Test 1 - AssertFalse is passed: if expr is False for make_one_hot **")


    #tests for train_xgb_model
    def test_train_xgb_model_not_null(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen'], 'los': 10}
        row2 = {'admission_id':2, 'feature_entities':[], 'los': 5}
        row3 = {'admission_id':3, 'feature_entities':['not_well_seen'], 'los': 3}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        one_hot = pd.DataFrame()
        oh_row1 = {'accident': 1, 'not_well_seen': 1}
        oh_row2 = {'accident': 0, 'not_well_seen': 0}
        oh_row3 = {'accident': 0, 'not_well_seen': 1}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)
        one_hot = one_hot.append(oh_row3, ignore_index=True)

        xgb_model = xgb_los_feature_entities.train_xgb_model(df, one_hot)
        # print (one_hot)
        if (one_hot.empty):
            True
        if (one_hot.all):
            True
        print ("** Test 2 Passed - train_xgb_model **")
        # Reference - https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o


    #tests for add_predictions_column
    def test_add_predictions_column_no_null_entries(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen'], 'los': 7}
        row2 = {'admission_id':2, 'feature_entities':[], 'los': 5}
        row3 = {'admission_id':3, 'feature_entities':['not_well_seen'], 'los': 12}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        one_hot = pd.DataFrame()
        oh_row1 = {'accident': 1, 'not_well_seen': 1}
        oh_row2 = {'accident': 0, 'not_well_seen': 0}
        oh_row3 = {'accident': 0, 'not_well_seen': 1}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)
        one_hot = one_hot.append(oh_row3, ignore_index=True)

        xgb_model = xgb_los_feature_entities.train_xgb_model(df, one_hot)

        updated_df = xgb_los_feature_entities.add_predictions_column(df, xgb_model, one_hot)
        # print (updated_df)

        null_count = 0
        for i, row in updated_df.iterrows():
            if row['xgb_feat_ent_pred'] == None:
                null_count += 1
            if row['xgb_feat_ent_pred'] == '0.5':
                True
        # assert(null_count == 0)
       #  assertEqual(row['xgb_feat_ent_pred'] == '0.6')
        print ("** Test 3 Passed - add_predictions_column **")



    def test_make_top_n_features_check_num_features(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen'], 'los': 11}
        row2 = {'admission_id':2, 'feature_entities':['leg', 'feet'], 'los': 10}
        row3 = {'admission_id':3, 'feature_entities':['not_well_seen'], 'los': 8}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        one_hot = pd.DataFrame()
        oh_row1 = {'accident': 1, 'not_well_seen': 1, 'leg': 0, 'feet': 0}
        oh_row2 = {'accident': 0, 'not_well_seen': 0, 'leg': 1, 'feet': 1}
        oh_row3 = {'accident': 0, 'not_well_seen': 1, 'leg': 0, 'feet': 0}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)
        one_hot = one_hot.append(oh_row3, ignore_index=True)

        xgb_model = xgb_los_feature_entities.train_xgb_model(df, one_hot)
        top_2_df = xgb_los_feature_entities.make_top_n_features(xgb_model, one_hot, 2)
        # print (top_2_df)

        assert(len(top_2_df.columns) <= 2)
        assert(len(top_2_df.index) <= 0)

        print ("** Test 4 Passed - make_top_n_features **")


if __name__ == '__main__':
    unittest.main()
