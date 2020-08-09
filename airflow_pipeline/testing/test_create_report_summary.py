import sys
sys.path.insert(0,'..')

import unittest
import pandas as pd
import pickle
import create_report_summary
from workflow_read_and_write import standard_read_from_db

class SomeCallableTest(unittest.TestCase):
    
    # tests for make_patient_summary
    def test_make_patient_summary_check_columns(self):
        df = pd.DataFrame()
        row = {
                'patient_id': 1, 
                'readmission':1, 
                'admittime': 'Mon, 07 May 2131 00:00:00 GMT',
                'icd_codes': [5,8,72],
                'los': 5,
                'age': 32,
                'gender': 'M',
                'insurance':'MEDICAID',
                'diagnosis':'heart attack',
              }
        df = df.append(row, ignore_index=True)

        summary_df = create_report_summary.make_patient_summary(df)
        expected_columns = [
                'patient_id', 
                'readmission_count', 
                '12_month_admission_count', 
                'los_avg',
                'icd_codes',
                'age', 
                'gender', 
                'insurance_type',
                'dx_description']

        missing = 0
        for column in expected_columns:
            if column not in summary_df.columns:
                missing += 1
                print(column)

        assert(missing == 0)

    def test_make_patient_summary_two_entries_one_patient(self):
        df = pd.DataFrame()
        row1 = {
                'patient_id': 1,
                'readmission':0,
                'admittime': 'Mon, 07 May 2131 00:00:00 GMT',
                'icd_codes': [5,8,72],
                'los': 5,
                'age': 32,
                'gender': 'M',
                'insurance':'MEDICAID',
                'diagnosis':'heart attack'
               }
        row2 = {
                'patient_id': 1,
                'readmission':1,
                'admittime': 'Mon, 14 May 2131 00:00:00 GMT',
                'icd_codes': [5,35,72],
                'los': 3,
                'age': 32,
                'gender': 'M',
                'insurance':'MEDICAID',
                'diagnosis':'heart attack'
               }
        df = df.append(row1, ignore_index = True)
        df = df.append(row2, ignore_index = True)

        summary_df = create_report_summary.make_patient_summary(df)

        # check if los_avg and icd_codes columns are combined from the two separate entries in df

        expected_los_avg = 4
        expected_icd_codes = [5, 8, 72, 35]

        actual_los_avg = summary_df['los_avg'][0]
        actual_icd_codes = summary_df['icd_codes'][0]

        assert(actual_los_avg == expected_los_avg and actual_icd_codes == expected_icd_codes)

    def test_make_patient_summary_multiple_patients(self):
        df = pd.DataFrame()
        row1 = {
                'patient_id': 1,
                'readmission':1,
                'admittime': 'Mon, 07 May 2131 00:00:00 GMT',
                'icd_codes': [5,8,72],
                'los': 5,
                'age': 32,
                'gender': 'M',
                'insurance':'MEDICAID',
                'diagnosis':'heart attack'
               }
        row2 = {
                'patient_id': 2,
                'readmission':1,
                'admittime': 'Mon, 07 May 2131 00:00:00 GMT',
                'icd_codes': [9,20],
                'los': 3,
                'age': 25,
                'gender': 'F',
                'insurance':'UNINSURED',
                'diagnosis':'panic attacks'
               }
        df = df.append(row1, ignore_index = True)
        df = df.append(row2, ignore_index = True)

        summary_df = create_report_summary.make_patient_summary(df)

        #figure out some stuff
        expected_icd_codes_1 = [5,8,72]
        expected_icd_codes_2 = [9,20]
        expected_los_avg_1 = 5
        expected_los_avg_2 = 3

        actual_icd_codes_1 = summary_df['icd_codes'][0]
        actual_icd_codes_2 = summary_df['icd_codes'][1]
        actual_los_avg_1 = summary_df['los_avg'][0]
        actual_los_avg_2 = summary_df['los_avg'][1]

        assert(actual_icd_codes_1 == expected_icd_codes_1 and actual_icd_codes_2 == expected_icd_codes_2 and actual_los_avg_1 == expected_los_avg_1 and actual_los_avg_2 == expected_los_avg_2)

    # tests for make_hospital_summary
    def test_make_hospital_summary_check_columns(self):
        df = pd.DataFrame()
        row = {
                'patient_id': 1,
                'readmission':1,
                'admittime': 'Mon, 07 May 2131 00:00:00 GMT',
                'icd_codes': [5,8,72],
                'los': 5,
                'age': 32,
                'gender': 'M',
                'insurance':'MEDICAID',
                'diagnosis':'heart attack',
              }
        df = df.append(row, ignore_index = True)

        word2vec_pickle = standard_read_from_db('word2vec')
        readmission_word2vec_pickle = standard_read_from_db('readmission_word2vec')
        word2vec_model = pickle.loads(word2vec_pickle)
        readmission_word2vec_model = pickle.loads(readmission_word2vec_pickle)
        lda_topics = [(0, '0.008*"2**]_medical_condition:_year_old" + 0.007*"4**]_medical_condition:_year_old" + 0.007*"[**hospital_4**]_medical_condition:_year" + 0.001*"chest_(pa_lat)_clip_[**clip" + 0.001*"reason_for_this_examination:_s/p" + 0.001*"chamber_size_and_free_wall"'), (1, '0.009*"condition:_year_old_man_with" + 0.008*"chest_(portable_ap)_clip_[**clip" + 0.008*"[**hospital_2**]_medical_condition:_year" + 0.003*"reason_for_this_examination:_please" + 0.002*"head_w/o_contrast_clip_[**clip" + 0.001*"reason_for_this_examination:_assess"'), (2, '0.011*"medical_condition:_year_old_man" + 0.001*"with_reason_for_this_examination:" + 0.001*"for_this_examination:_eval_for" + 0.001*"w/contrast_clip_[**clip_number_(radiology)" + 0.001*"old_man_with_reason_for" + 0.001*"with_dr._[**last_name_(stitle)"'), (3, '0.008*"(portable_ap)_clip_[**clip_number" + 0.003*"w/o_contrast_clip_[**clip_number" + 0.002*"reason_for_this_examination:_eval" + 0.002*"contraindications_for_contrast_final_report" + 0.002*"3**]_medical_condition:_year_old" + 0.002*"lat)_clip_[**clip_number_(radiology)"'), (4, '0.008*"ap)_clip_[**clip_number_(radiology)" + 0.006*"medical_condition:_year_old_woman" + 0.005*"condition:_year_old_woman_with" + 0.003*"contrast_clip_[**clip_number_(radiology)" + 0.003*"reason_for_this_examination:_r/o" + 0.002*"[**hospital_3**]_medical_condition:_year"')]

        top_n_dict = {}

        top_n_feat_los_df = pd.DataFrame()
        row = {'heart_attack': 0, 'fractured_rib': 1, 'backpain': 1, 'lack_of_exercise': 0, 'pneumonia':1}
        top_n_feat_los_df = top_n_feat_los_df.append(row, ignore_index = True)
        top_n_dict['top_n_feat_los_df'] = top_n_feat_los_df

        top_n_neg_feat_los_df = pd.DataFrame()
        row = {'no_heart_attack':1, 'no_fractured_rib': 0, 'no_backpain':0, 'no_lack_of_exercise': 1, 'pneumonia': 0}
        top_n_neg_feat_los_df = top_n_neg_feat_los_df.append(row, ignore_index = True)
        top_n_dict['top_n_neg_feat_los_df'] = top_n_neg_feat_los_df

        top_n_med_los_df = pd.DataFrame()
        row = {'advil': 1, 'tylenol': 0, 'placebo': 1, 'nyquil': 0, 'dayquil': 0}
        top_n_med_los_df = top_n_med_los_df.append(row, ignore_index = True)
        top_n_dict['top_n_med_los_df'] = top_n_med_los_df

        top_n_neg_med_los_df = pd.DataFrame()
        row = {'advil': 0, 'tylenol': 1, 'placebo': 0, 'nyquil': 1, 'dayquil': 1}
        top_n_neg_med_los_df = top_n_neg_med_los_df.append(row, ignore_index = True)
        top_n_dict['top_n_neg_med_los_df'] = top_n_neg_med_los_df

        top_n_feat_readm_df = pd.DataFrame()
        row = {'heart_attack': 0, 'fractured_rib': 1, 'backpain': 1, 'lack_of_exercise': 0, 'pneumonia':1}
        top_n_feat_readm_df.append(row, ignore_index = True)
        top_n_dict['top_n_feat_readm_df'] = top_n_feat_readm_df

        top_n_neg_feat_readm_df = pd.DataFrame()
        row = {'no_heart_attack':1, 'no_fractured_rib': 0, 'no_backpain':0, 'no_lack_of_exercise': 1, 'pneumonia': 0}
        top_n_neg_feat_readm_df = top_n_neg_feat_readm_df.append(row, ignore_index = True)
        top_n_dict['top_n_neg_feat_readm_df'] = top_n_neg_feat_readm_df

        top_n_med_readm_df = pd.DataFrame()
        row = {'advil': 1, 'tylenol': 0, 'placebo': 1, 'nyquil': 0, 'dayquil': 0}
        top_n_med_readm_df = top_n_med_readm_df.append(row, ignore_index = True)
        top_n_dict['top_n_med_readm_df'] = top_n_med_readm_df

        top_n_neg_med_readm_df = pd.DataFrame()
        row = {'advil': 0, 'tylenol': 1, 'placebo': 0, 'nyquil': 1, 'dayquil': 1}
        top_n_neg_med_readm_df = top_n_neg_med_readm_df.append(row, ignore_index = True)
        top_n_dict['top_n_neg_med_readm_df'] = top_n_neg_med_readm_df

        hospital_summary_df = create_report_summary.make_hospital_summary(df, top_n_dict, readmission_word2vec_model, word2vec_model, lda_topics)

        expected_columns = ['total_admissions', 'total_readmissions', 'top_10_icd_codes_readmission_count', 'overall_los_avg', 'Insurance: MEDICAID los_avg', 'Gender: M los_avg', 'top_10_icd_codes_from_los', 'top_5_terms_feat_los', 'top_5_terms_neg_feat_los', 'top_5_terms_med_los', 'top_5_terms_neg_med_los', 'top_5_terms_feat_readmissions', 'top_5_terms_neg_feat_readmissions', 'top_5_terms_med_readmissions', 'top_5_terms_neg_med_readmissions']

        missing = 0
        for col in expected_columns:
            if col not in hospital_summary_df.columns:
                missing += 1

        assert(missing == 0)

if __name__ == '__main__':
    unittest.main()
