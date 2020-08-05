import sys
sys.path.insert(0,'..')

import unittest
import add_labeled_notes_column
import pandas as pd

class SomeCallableTest(unittest.TestCase):

    # tests for get_line_length_array
    def test_get_length_array_multiple_notes_varying_lengths(self):
        df = pd.DataFrame()
        row1 = {'ner_cleaned_notes': 'The quick brown fox \n jumped over the \n log'}
        row2 = {'ner_cleaned_notes': 'test test 12 check'}
        row3 = {'ner_cleaned_notes': 'Down by the bay \n Where the watermelons grow'}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)
        
        length_array = add_labeled_notes_column.get_line_length_array(df)
        expected_array = [3,1,2]

        assert(length_array == expected_array)

    # tests for get_note_lines_from_file
    def test_get_note_lines_from_files_standard(self):
        lines = add_labeled_notes_column.get_note_lines_from_file()
        expected = ['The quick brown fox \n',' jumped over the \n', ' log\n', 'test test 12 check\n', 'Down by the bay \n', ' Where the watermelons grow\n']
        assert(lines == expected)

    # tests for make_column
    def test_make_column_no_entities(self):
        df = pd.DataFrame()
        row1 = {'ner_cleaned_notes': 'The quick brown fox \n jumped over the \n log\n'}
        row2 = {'ner_cleaned_notes': 'test test 12 check\n'}
        row3 = {'ner_cleaned_notes': 'Down by the bay \n Where the watermelons grow\n'}
        df = df.append(row1, ignore_index=True)
        df = df.append(row2, ignore_index=True)
        df = df.append(row3, ignore_index=True)
        
        length_array = [3, 1, 2]
        lines = ['The quick brown fox \n',' jumped over the \n', ' log\n','test test 12 check\n','Down by the bay \n',' Where the watermelons grow\n']
        
        #Since no entities are present and the notes are both cleaned the same way, the columns for ner_cleaned_notes and the ner_labeled_notes should be the same
        column = add_labeled_notes_column.make_column(lines, length_array)
        expected = df['ner_cleaned_notes'].to_list()
        assert(column == expected)


if __name__ == '__main__':
    unittest.main()
