import sys
sys.path.insert(0,'..')

import unittest
import create_lda_model

class SomeCallableTest(unittest.TestCase):
    
    # tests for generate_ngrams
    def test_generate_ngrams_standard(self):
        test_string = 'The quick brown fox jumped over the log. It was a hot day.'
        n = 5
        ngrams = create_lda_model.generate_ngrams(test_string, n)
        expected = ['the_quick_brown_fox_jumped', 'quick_brown_fox_jumped_over', 'brown_fox_jumped_over_the', 'fox_jumped_over_the_log.', 'jumped_over_the_log._was', 'over_the_log._was_hot', 'the_log._was_hot_day.']
        assert(ngrams == expected)

    # tests for create_ngram_tokens
    def test_create_ngram_tokens_standard(self):
        test_text = 'The quick brown fox jumped over the log. It was a hot day. This is a test sentence with a lot of words.'
        ngram_tokens = create_lda_model.create_ngram_tokens(test_text)
        expected = ['the_quick_brown_fox_jumped','quick_brown_fox_jumped_over','brown_fox_jumped_over_the','fox_jumped_over_the_log.','was_hot_day.','this_test_sentence_with_lot','test_sentence_with_lot_words.']
        print(ngram_tokens)
        print(expected)
        assert(ngram_tokens==expected)

    # tests for make_model
    def test_make_model_check_non_null_output(self):
        tokens = ['the_quick_brown_fox_jumped','quick_brown_fox_jumped_over','brown_fox_jumped_over_the','fox_jumped_over_the_log.','was_hot_day.','this_test_sentence_with_lot','test_sentence_with_lot_words.']
        dictionary, corpus, lda_model = create_lda_model.make_model(tokens)
        assert(dictionary is not None and corpus is not None and lda_model is not None)

if __name__ == '__main__':
    unittest.main()
