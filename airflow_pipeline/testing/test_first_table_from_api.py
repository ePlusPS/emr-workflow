import sys
sys.path.insert(0,'..')

import unittest
import first_table_from_api
import requests
class SomeCallableTest(unittest.TestCase):

    # tests for get_all_notes
    def test_notes_fields_are_present(self):
        notes = first_table_from_api.get_all_notes()
        note = notes[0]
        keys = list(note.keys())
        expected_keys = ['row_id', 'text', 'admittime', 'dischtime', 'deathtime', 'patient_id','admission_id', 'insurance', 'language', 'religion','marital_status','ethnicity', 'diagnosis']
        
        check_vals = True
        if len(keys) != len(expected_keys):
            check_vals = False
        else:
            for key in keys:
                if key not in expected_keys:
                    check_vals = False
                    break
        
        assert(check_vals)


    # tests for get_admissions
    def test_admissions_fields_are_present(self):
        admissions = first_table_from_api.get_admissions()
        admission = admissions[0]
        keys = list(admission.keys())
        expected_keys = ['admission_id', 'admittime', 'dischtime', 'deathtime', 'patient_id', 'insurance', 'language', 'religion', 'marital_status', 'ethnicity', 'diagnosis']
        
        check_vals = True
        if len(keys) != len(expected_keys):
            check_vals = False
        else:
            for key in keys:
                if key not in expected_keys:
                    check_vals = False
                    break
        
        assert(check_vals)
    
    # tests for get_icd_codes
    def test_icd_fields_are_present(self):
        icd_codes = first_table_from_api.get_icd_codes()
        icd_code = icd_codes[0]
        keys = list(icd_code.keys())
        expected_keys = ['admission_id', 'icd_code']

        check_vals = True
        if len(keys) != len(expected_keys):
            check_vals = False
        else:
            for key in keys:
                if key not in expected_keys:
                    check_vals = False
                    break

        assert(check_vals)

    # tests for get_patients
    def test_patients_fields_are_present(self):
        patients = first_table_from_api.get_patients()
        patient = patients[0]
        keys = list(patient.keys())
        expected_keys = ['row_id', 'patient_id', 'gender', 'dob']

        check_vals = True
        if len(keys) != len(expected_keys):
            check_vals = False
        else:
            for key in keys:
                if key not in expected_keys:
                    check_vals = False
                    break

        assert(check_vals)
    
    # tests for combine_notes_and_admissions_and_codes
    def test_combine_notes_admissions_codes_columns_are_present(self):
        admissions = first_table_from_api.get_admissions()
        admissions = admissions[:100]
        
        notes_resp = requests.get('http://10.32.22.6:56733/noteevents/page/1')
        notes = notes_resp.json()['json_notes']

        icd_codes = get_icd_codes()
        patients = get_patients()

        combined = combine_notes_and_admissions_and_codes(admissions, notes, icd_codes, patients)

        combined_admission = combined[0]
        keys = list(combined_admission.keys())

        expected_keys = ['admission_id', 'admittime', 'dischtime', 'deathtime', 'patient_id', 'insurance', 'language', 'religion', 'marital_status', 'ethnicity', 'diagnosis','notes','icd_codes', 'gender','dob']

        check_vals = True
        if len(keys) != len(expected_keys):
            check_vals = False
        else:
            for key in keys:
                if key not in expected_keys:
                    check_vals = False
                    break
        
        assert(check_vals)

if __name__ == '__main__':
    unittest.main()
