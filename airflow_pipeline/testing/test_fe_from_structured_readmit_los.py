import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import fe_from_structured_readmit_los
import pandas as pd

class SomeCallableTest(unittest.TestCase):

    def setUp(self):
        self.df = pd.read_parquet('500_test_structured.parquet')
        self.df.drop(['index', 'age', 'los', 'readmission', 'death_time_present'], axis=1, inplace=True)

    # tests for add_los_age_and_binary_deathtime_columns 
    # Input is dataframe with these columns:
    # ['admission_id', 'admittime', 'deathtime', 'diagnosis', 'dischtime','ethnicity', 'insurance', 'language', 'marital_status', 'patient_id','religion', 'notes', 'icd_codes', 'gender', 'dob']
    # times are in this format: 'Mon, 07 May 2131 00:00:00 GMT'

    def test_los_calculation(self):
        df = pd.DataFrame()
        row = {'admission_id':1,
                'admittime' :'Mon, 07 May 2131 00:00:00 GMT', 
                'deathtime': None,
                'diagnosis': 'lupus',
                'dischtime':'Thurs, 10 May 2131 00:00:00 GMT',
                'ethnicity': 'HISPANIC',
                'insurance': 'PRIVATE',
                'language': 'SPANISH',
                'marital_status': 'SINGLE',
                'patient_id': 500,
                'religion': 'UNSPECIFIED',
                'notes': '',
                'icd_codes':[5,6,7],
                'gender': 'F',
                'dob': 'Sat, 07 May 2101 00:00:00 GMT'}
        df = df.append(row, ignore_index=True)
        updated_df = fe_from_structured_readmit_los.add_los_age_and_binary_deathtime_columns(df)

        los = updated_df.iloc[0]['los']
        expected_los = 3
        assert(los == expected_los)

    def test_age_calculation(self):
        df = pd.DataFrame()
        row = {'admission_id':1,
                'admittime' :'Mon, 07 May 2131 00:00:00 GMT',
                'deathtime': None,
                'diagnosis': 'lupus',
                'dischtime':'Thurs, 10 May 2131 00:00:00 GMT',
                'ethnicity': 'HISPANIC',
                'insurance': 'PRIVATE',
                'language': 'SPANISH',
                'marital_status': 'SINGLE',
                'patient_id': 500,
                'religion': 'UNSPECIFIED',
                'notes': '',
                'icd_codes':[5,6,7],
                'gender': 'F',
                'dob': 'Sat, 07 May 2101 00:00:00 GMT'}
        df = df.append(row, ignore_index=True)
        updated_df = fe_from_structured_readmit_los.add_los_age_and_binary_deathtime_columns(df)

        age = updated_df['age']
        expected_age = 30
        assert(age == expected_age)

    def test_death_time_not_present(self):
        df = pd.DataFrame()
        row = {'admission_id':1,
                'admittime' :'Mon, 07 May 2131 00:00:00 GMT',
                'deathtime': None,
                'diagnosis': 'lupus',
                'dischtime': 'Thurs, 10 May 2131 00:00:00 GMT',
                'ethnicity': 'HISPANIC',
                'insurance': 'PRIVATE',
                'language': 'SPANISH',
                'marital_status': 'SINGLE',
                'patient_id': 500,'religion': 
                'UNSPECIFIED','notes': '',
                'icd_codes':[5,6,7],
                'gender': 'F',
                'dob': 'Sat, 07 May 2101 00:00:00 GMT'}
        df = df.append(row, ignore_index=True)
        updated_df = fe_from_structured_readmit_los.add_los_age_and_binary_deathtime_columns(df)

        assert(updated_df['death_time_present'] == False)

    def test_death_time_present(self):
        df = pd.DataFrame()
        row = {'admission_id':1,
                'admittime' :'Mon, 07 May 2131 00:00:00 GMT',
                'deathtime': None,
                'diagnosis': 'lupus',
                'dischtime': 'Thurs, 10 May 2131 00:00:00 GMT',
                'ethnicity': 'HISPANIC',
                'insurance': 'PRIVATE',
                'language': 'SPANISH',
                'marital_status': 'SINGLE',
                'patient_id': 500,
                'religion': 'UNSPECIFIED',
                'notes': '',
                'icd_codes':[5,6,7],
                'gender': 'F',
                'dob': 'Sat, 07 May 2101 00:00:00 GMT'}
        df = df.append(row, ignore_index=True)
        updated_df = fe_from_structured_readmit_los.add_los_age_and_binary_deathtime_columns(df)

        assert(updated_df['death_time_present'] == True)


    # tests for compare_times_for_readmission
      # test with an admittime greater than a discharge time, hence difference will be negative, uses absolute value
    def test_readmission_flag_admit_greater_than_discharge(self):
        prev_dischtime = pd.to_datetime('Thurs, 10 May 2131 00:00:00 GMT')
        curr_admittime = pd.to_datetime('Wed, 09 May 2131 00:00:00 GMT')
        readmission = fe_from_structured_readmit_los.compare_times_for_readmission(curr_admittime, prev_dischtime)
        assert(readmision == True)

      # test with the difference between last dischtime and current admittime is between 30 and 31 days
    def test_readmission_flag_difference_between_30_and_31_days(self):
        prev_dischtime = pd.to_datetime('Thurs, 10 May 2131 00:00:00 GMT')
        curr_admittime = pd.to_datetime('Sat, 09 June 2131 01:00:00 GMT')
        readmission = fe_from_structured_readmit_los.compare_times_for_readmission(curr_admittime, prev_dischtime)
        assert(readmission == False)

      # test the difference qualifying for being flagged as a readmission
    def test_readmission_flag_standard(self):
        prev_dischtime = pd.to_datetime('Thurs, 10 May 2131 00:00:00 GMT')
        curr_admittime = pd.to_datetime('Fri, 11 May 2131 00:00:00 GMT')
        readmission = fe_from_structured_readmit_los.compare_times_for_readmission(curr_admittime, prev_dischtime)
        assert(readmission == True)

      # test with the difference being 0
    def test_readmission_flag_no_difference(self):
        prev_dischtime = pd.to_datetime('Thurs, 10 May 2131 00:00:00 GMT')
        curr_admittime = pd.to_datetime('Thurs, 10 May 2131 00:00:00 GMT')
        readmission = fe_from_structured_readmit_los.compare_times_for_readmission(curr_admittime, prev_dischtime)
        assert(readmission==True)

      # test with the difference being greater than a readmission
    def test_readmision_flag_not_a_readmission(self):
        prev_dischtime = pd.to_datetime('Thurs, 10 May 2131 00:00:00 GMT')
        curr_admittime = pd.to_datetime('Sat, 30 June 2131 00:00:00 GMT')
        readmission = fe_from_structured_readmit_los.compare_times_for_readmission(curr_admittime, prev_dischtime)
        assert(readmission == False)

    # tests for add_readmission_column
    def test_add_readmission_column(self):
        df = pd.DataFrame()
        row1 = {'admission_id': 1, 'admittime': 'Mon, 07 May 2131 00:00:00 GMT', 'deathtime': None, 'diagnosis':'lupus', 'dischtime': 'Thurs, 10 May 2131 00:00:00 GMT', 'ethnicity': 'HISPANIC', 'insurance': 'PRIVATE', 'language': 'SPANISH', 'marital_status': 'SINGLE', 'patient_id': 500, 'religion': 'UNSPECIFIED', 'notes': '', 'icd_codes':[5,6,7], 'gender': 'F', 'dob': 'Sat, 07 May 2101 00:00:00 GMT'}
        row2 = {'admission_id': 2, 'admittime': 'Sun, 13 May 2131 00:00:00 GMT', 'deathtime': None, 'diagnosis':'lupus', 'dischtime': 'Tues, 15 May 2131 00:00:00 GMT', 'ethnicity': 'HISPANIC', 'insurance': 'PRIVATE', 'language': 'SPANISH', 'marital_status': 'SINGLE', 'patient_id': 500, 'religion': 'UNSPECIFIED', 'notes': '', 'icd_codes':[5,6,7], 'gender': 'F', 'dob': 'Sat, 07 May 2101 00:00:00 GMT'}
        row3 = {'admission_id': 3, 'admittime': 'Thurs, 05 July 2131 00:00:00 GMT', 'deathtime': None, 'diagnosis':'lupus', 'dischtime': 'Sat, 07 July 2131 00:00:00 GMT', 'ethnicity': 'HISPANIC', 'insurance': 'PRIVATE', 'language': 'SPANISH', 'marital_status': 'SINGLE', 'patient_id': 500, 'religion': 'UNSPECIFIED', 'notes': '', 'icd_codes':[5,6,7], 'gender': 'F', 'dob': 'Sat, 07 May 2101 00:00:00 GMT'}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        updated_df = fe_from_structured_readmit_los.add_readmission_column(df)
        readmission_column = updated_df['readmission']
        readm_list = readmission_column.to_list()
        expected_list = [False, True, False]

        assert(readm_list == expected_list)

if __name__ == '__main__':
    unittest.main()
