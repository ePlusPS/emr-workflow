import sys
sys.path.insert(0,'..')

import unittest
import lda_topics_per_note
import pandas as pd

class SomeCallableTest(unittest.TestCase):

    # tests for generate_ngrams
    def test_generate_ngrams_standard(self):
        test_string = 'The quick brown fox jumped over the log. It was a hot day.'
        n = 5
        ngrams = lda_topics_per_note.generate_ngrams(test_string, n)
        expected = ['the_quick_brown_fox_jumped', 'quick_brown_fox_jumped_over', 'brown_fox_jumped_over_the', 'fox_jumped_over_the_log.', 'jumped_over_the_log._was', 'over_the_log._was_hot', 'the_log._was_hot_day.']
        assert(ngrams == expected)

    # tests for create_ngram_tokens
    def test_create_ngram_tokens_standard(self):
        test_text = 'The quick brown fox jumped over the log. It was a hot day. This is a test sentence with a lot of words.'
        ngram_tokens = lda_topics_per_note.create_ngram_tokens(test_text)
        expected = ['the_quick_brown_fox_jumped','quick_brown_fox_jumped_over','brown_fox_jumped_over_the','fox_jumped_over_the_log.','was_hot_day.','this_test_sentence_with_lot','test_sentence_with_lot_words.']
        #print(ngram_tokens)
        #print(expected)
        assert(ngram_tokens==expected)

    # tests for clean_note
    def test_clean_note_remove_characters(self):
        test = '\n\n asdffdsa +|||__**[]][())(...,,,:::'
        test_cleaned = lda_topics_per_note.clean_note(test)
        expected = 'asdffdsa'
        assert(test_cleaned == expected)
    
    # tests for make_lda_topics_list
    def test_make_lda_topics_list_standard(self):
        topics = [(0, '0.008*"2**]_medical_condition:_year_old" + 0.007*"4**]_medical_condition:_year_old" + 0.007*"[**hospital_4**]_medical_condition:_year" + 0.001*"chest_(pa_lat)_clip_[**clip" + 0.001*"reason_for_this_examination:_s/p" + 0.001*"chamber_size_and_free_wall"'), (1, '0.009*"condition:_year_old_man_with" + 0.008*"chest_(portable_ap)_clip_[**clip" + 0.008*"[**hospital_2**]_medical_condition:_year" + 0.003*"reason_for_this_examination:_please" + 0.002*"head_w/o_contrast_clip_[**clip" + 0.001*"reason_for_this_examination:_assess"'), (2, '0.011*"medical_condition:_year_old_man" + 0.001*"with_reason_for_this_examination:" + 0.001*"for_this_examination:_eval_for" + 0.001*"w/contrast_clip_[**clip_number_(radiology)" + 0.001*"old_man_with_reason_for" + 0.001*"with_dr._[**last_name_(stitle)"'), (3, '0.008*"(portable_ap)_clip_[**clip_number" + 0.003*"w/o_contrast_clip_[**clip_number" + 0.002*"reason_for_this_examination:_eval" + 0.002*"contraindications_for_contrast_final_report" + 0.002*"3**]_medical_condition:_year_old" + 0.002*"lat)_clip_[**clip_number_(radiology)"'), (4, '0.008*"ap)_clip_[**clip_number_(radiology)" + 0.006*"medical_condition:_year_old_woman" + 0.005*"condition:_year_old_woman_with" + 0.003*"contrast_clip_[**clip_number_(radiology)" + 0.003*"reason_for_this_examination:_r/o" + 0.002*"[**hospital_3**]_medical_condition:_year"')]
        topics_list = lda_topics_per_note.make_lda_topics_list(topics)
        expected = ['2**]_medical_condition:_year_old','4**]_medical_condition:_year_old', '[**hospital_4**]_medical_condition:_year', 'chest_(pa_lat)_clip_[**clip', 'reason_for_this_examination:_s/p', 'chamber_size_and_free_wall', 'condition:_year_old_man_with', 'chest_(portable_ap)_clip_[**clip','reason_for_this_examination:_assess','medical_condition:_year_old_man', 'with_reason_for_this_examination:', 'for_this_examination:_eval_for', 'w/contrast_clip_[**clip_number_(radiology)', 'old_man_with_reason_for', 'with_dr._[**last_name_(stitle)', '(portable_ap)_clip_[**clip_number', 'w/o_contrast_clip_[**clip_number', 'reason_for_this_examination:_eval', 'contraindications_for_contrast_final_report', '3**]_medical_condition:_year_old','lat)_clip_[**clip_number_(radiology)','ap)_clip_[**clip_number_(radiology)', 'medical_condition:_year_old_woman','condition:_year_old_woman_with','contrast_clip_[**clip_number_(radiology)', 'reason_for_this_examination:_r/o', '[**hospital_3**]_medical_condition:_year', '[**hospital_2**]_medical_condition:_year', 'reason_for_this_examination:_please', 'head_w/o_contrast_clip_[**clip']
        
        mismatch_count = 0
        for topic in topics_list:
            if topic not in expected:
                mismatch_count += 1

        assert(mismatch_count == 0)

    # tests for create_lda_ngrams_column
    def test_create_lda_ngrams_column_standard(self):
        df = pd.DataFrame()
        lda_topics_list = ['blood_pressure_greater_than_100', 'fractured_rib_and_broken_femur']
        row1 = {'admission_id':1,'notes':'blood pressure greater is than 100, has a fractured rib and broken femur'}
        row2 = {'admission_id':2,'notes':'often faints during physical exertion'}
        row3 = {'admission_id':3,'notes':'has a fractured rib and broken femur'}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)

        lda_ngrams_column = lda_topics_per_note.create_lda_ngrams_column(df, lda_topics_list)
        expected = [['blood_pressure_greater_than_100','fractured_rib_and_broken_femur'],[],['fractured_rib_and_broken_femur']]
        print(lda_ngrams_column)
        print(expected)
        assert(lda_ngrams_column == expected)




if __name__ == '__main__':
    unittest.main()
