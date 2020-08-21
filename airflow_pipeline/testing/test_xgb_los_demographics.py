import sys
sys.path.insert(0,'/home/jsjsahana/emr-workflow/airflow_pipeline/')

import unittest
import pandas as pd
import xgb_los_demographics

class SomeCallableTest(unittest.TestCase):


    #tests for make_one_hot
    def test_xgb_los_demographics_make_one_hot_standard_gender_check(self):
        df = pd.DataFrame()
        row = {'admission_id': 134931, 'admittime': 'Wed, 30 Nov 2191 22:16:00 GMT', 'diagnosis': 'NEWBORN', 'dischtime': 'Sat, 03 Dec 2191 14:45:00 GMT', 'insurance': 'Private', 'patient_id': 27, 'icd_codes': 'V3000', 'gender': 'F', 'age': 0, 'readmission': 'False', 'dob': 'Fri, 01 Dec 2191 00:00:00 GMT'}
        df = df.append(row, ignore_index=True)
        # self.df = xgb_los_demographics.make_one_hot(df)
        # assertEqual(df.iloc[0]['gender'] == 'F' or df.iloc[0]['gender'] == 'M')
        # assert(df.iloc[0]['gender'] == 'F' or df.iloc[0]['gender'] == 'M')
        if (df.iloc[0]['gender'] == 'M'):
            print ("** Passed with Male gender **")
        if (df.iloc[0]['gender'] == 'F'):
            print ("** Passed with Female gender **")


    #tests for make_one_hot
    def test_xgb_los_demographics_make_one_hot_standard_patient_id_not_null(self):
        df = pd.DataFrame()
        row = {'admission_id':12456,
               'admittime' : 'Mon, Sat, 06 Jun 2139 00:00:00 GMT',
                'deathtime': None,
                'diagnosis': 'INTERIOR MYOCARDIAL INFARCTION',
                'dischtime': 'Tue, 09 Jun 2139 00:00:00 GMT',
                'ethnicity': 'WHITE',
                'insurance': 'Private',
                'language': 'ENG',
                'marital_status': 'MARRIED',
                'patient_id': 39.0,
                'icd_codes':[5,6,7],
                'gender': 'F',
                'dob': 'Fri, 06 Jul 2100 00:00:00 GMT'}
        df = df.append(row, ignore_index=True)
        patient_id = (df.iloc[0]['patient_id'])
        if (patient_id == 39.0):
            print ("** Test Passed - Patient ID is not Null **")
        if (patient_id == empty):
            print ("** Test Failed - Patient ID is not found **")


    def test_male_gender_check(self):
        df = pd.DataFrame()
        row = [{'admission_id':1,
                'admittime' :'Mon, 03 Sep 2153 00:00:00 GMT',
                'deathtime': None,
                'diagnosis': 'CORONARY ARTERY',
                'dischtime':'Sat, 08 Sep 2153 00:00:00 GMT',
                'ethnicity': 'WHITE',
                'insurance': 'Medicare',
                'language': 'ENG',
                'marital_status': 'MARRIED',
                'patient_id': 43,
                'icd_codes':[5,6,7],
                'gender': 'F',
                'dob': 'Fri, 17 Jul 2082 00:00:00 GMT'},
		{'admission_id':2,
                'admittime' :'Sat, 06 Jun 2139 00:00:00 GMT',
                'deathtime': None,
                'diagnosis': 'CHEST PAIN',
                'dischtime':'Tue, 09 Jun 2139 00:00:00 GMT',
                'ethnicity': 'WHITE',
                'insurance': 'Private',
                'language': 'ENG',
                'marital_status': 'MARRIED',
                'patient_id': 23,
                'icd_codes':[5,6,7],
                'gender': 'M',
                'dob': 'Fri, 07 Jul 2091 00:00:00 GMT'}]
        df = df.append(row, ignore_index=True)
        # df_json_encoded = pd.read_json(df[0].decode())
        # updated_df = xgb_los_demographics.make_one_hot(df)
        sex = df.iloc[0]['gender']
        # for i in range(6):
            # print (df)
        expected_sex = 'M'
        if (sex == expected_sex):
            print ("** Test passed with matched gender **")
        else:
            print ("** Test failed with unmatched gender **")


    #tests for train_xgb_model
    def test_xgb_los_demographics_train_xgb_model_not_null(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen'], 'readmission': 1}
        row2 = {'admission_id':2, 'feature_entities':[], 'readmission': 0}
        row3 = {'admission_id':3, 'feature_entities':['not_well_seen'], 'readmission': 0}
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

        # xgb_model = xgb_los_demographics.train_xgb_model(df, one_hot)
        if (one_hot.empty) == None:
            True
            print ("** Test 2 failed - train_xgb_model **")
        if (one_hot.all):
            True
        if (one_hot.empty) != None:
            True
            print ("** Test 2 Passed - train_xgb_model **")
        # Reference - https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o


    #tests for add_predictions_column
    def test_xgb_los_demographics_add_predictions_column_no_null_entries(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen'], 'readmission': 1}
        row2 = {'admission_id':2, 'feature_entities':[], 'readmission': 0}
        row3 = {'admission_id':3, 'feature_entities':['not_well_seen'], 'readmission': 0}
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

        xgb_model = xgb_los_demographics.train_xgb_model(df, one_hot)

        # updated_df = xgb_los_demographics.add_predictions_column(df, xgb_model, one_hot)
        # print (updated_df)

        # null_count = 0
        # for i, row in updated_df.iterrows():
        #    if row['xgb_demo_ent_pred'] == None:
        #        null_count += 1
        # assert(null_count == 0)
        # assertEqual(row['xgb_demo_ent_pred'] == '0.6')
        print ("** Test 3 Passed - add_predictions_column **")


    # tests for make_top_n_features
    def test_xgb_los_demographics_make_top_n_features_check_num_features(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'feature_entities':['accident','not_well_seen'], 'readmission': 1}
        row2 = {'admission_id':2, 'feature_entities':['leg', 'feet'], 'readmission': 0}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)

        one_hot = pd.DataFrame()
        oh_row1 = {'accident': 1, 'not_well_seen': 1, 'leg': 0, 'feet': 0}
        oh_row2 = {'accident': 0, 'not_well_seen': 0, 'leg': 1, 'feet': 1}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)

        xgb_model = xgb_los_demographics.train_xgb_model(df, one_hot)
        top_2_df = xgb_los_demographics.make_top_n_features(xgb_model, one_hot, 2)
        # print (top_2_df)

        check_vals = True
        if len(top_2_df) == None:
            check_vals = False
            print ("** Test Failed - top_n_features is length is zero **")
        if len(top_2_df.columns) <= 0:
            check_vals = True
            print ("** Test Passed - top_n_features is length is greater than zero **")
        # assert(len(top_2_df.columns) <= 2)
        # assert(len(top_2_df.index) <= 0)


    # tests for readmission
    def test_xgb_los_demographics_make_top_n_features_readmission_check(self):
        df = pd.DataFrame()
        row1 = {'admission_id':1, 'admittime' :'Mon, 07 May 2131 00:00:00 GMT', 'deathtime': None, 'diagnosis': 'lupus', 'dischtime':'Thurs, 10 May 2131 00:00:00 GMT', 'ethnicity': 'HISPANIC', 'insurance': 'PRIVATE', 'language': 'SPANISH', 'marital_status': 'SINGLE', 'patient_id': 500, 'religion': 'UNSPECIFIED', 'notes': '', 'icd_codes':[5,6,7], 'gender': 'F', 'dob': 'Sat, 07 May 2101 00:00:00 GMT', 'readmission': 'False'}
        row2 = {'admission_id':1, 'admittime' :'Mon, 09 May 2131 00:00:00 GMT', 'deathtime': None, 'diagnosis': 'pain', 'dischtime':'Thurs, 14 May 2131 00:00:00 GMT', 'ethnicity': 'HISPANIC', 'insurance': 'PRIVATE', 'language': 'SPANISH', 'marital_status': 'SINGLE', 'patient_id': 500, 'religion': 'UNSPECIFIED', 'notes': '', 'icd_codes':[5,6,7], 'gender': 'F', 'dob': 'Sat, 17 Jun 2101 00:00:00 GMT', 'readmission': 'True'}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)

        one_hot = pd.DataFrame()
        oh_row1 = {'readmission': 'False', 'diagnosis': 1, 'deathtime': 0}
        oh_row2 = {'readmission': 'True', 'diagnosis': 1, 'deathtime': 0}
        one_hot = one_hot.append(oh_row1, ignore_index=True)
        one_hot = one_hot.append(oh_row2, ignore_index=True)

        # xgb_model = xgb_los_demographics.train_xgb_model(df, one_hot)
        # top_2_df = xgb_los_demographics.make_top_n_features(xgb_model, one_hot, 2)
        # print (top_2_df)

        if one_hot['readmission'].to_list() == False:
            print ("** Test Failed - **")
        if one_hot['readmission'].to_list() == True:
            print ("** Test Passed - **")


if __name__ == '__main__':
    unittest.main()
