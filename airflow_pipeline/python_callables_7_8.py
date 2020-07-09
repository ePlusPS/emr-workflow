from first_table_from_api import get_dataframe_from_apis
from fe_from_structured_readmit_los import create_structured_data_features
from word2vec_prep_clean_notes import clean_all_notes as word2vec_all_clean_notes
from word2vec_prep_tokenize_notes import tokenize_all_notes as word2vec_all_tokenize_notes
from create_word2vec_model import create_word2vec_model as word2vec_all_create_model
from fe_from_infection_keywords import infected_one_hot
from readmission_word2vec_prep_clean_notes import clean_readmission_notes
from readmission_word2vec_prep_tokenize_notes import tokenize_readmission_notes
from create_readmission_word2vec_model import create_word2vec_model as word2vec_readmission_create_model
from fe_from_readmission_keywords import readmission_one_hot
from ner_prep_clean_notes import clean_ner_notes
from make_all_note_lines_file import create_file
from inference_per_100000 import label_notes
from add_labeled_notes_column import create_labeled_notes_column
from create_entity_columns import create_entity_columns
from add_labeled_notes_column import create_labeled_notes_column
from xgb_los_demographics import make_predictions as make_predictions_los_demographics
from xgb_los_feature_entities import make_predictions as make_predictions_los_feat
from xgb_los_medication_entities import make_predictions as make_predictions_los_med
from xgb_los_neg_feature_entities import make_predictions as make_predictions_los_neg_feat
from xgb_los_neg_medication_entities import make_predictions as make_predictions_los_neg_med
from xgb_readmission_demographics import make_predictions as make_predictions_readm_demographics
from xgb_readmission_feature_entities import make_predictions as make_predictions_readm_feat
from xgb_readmission_medication_entities import make_predictions as make_predictions_readm_med
from xgb_readmission_neg_feature_entities import make_predictions as make_predictions_readm_neg_feat
from xgb_readmission_neg_medication_entities import make_predictions as make_predictions_readm_neg_med
from combine_los_estimates_tensorflow import make_predictions as make_predictions_tensorflow_los
from combine_readmission_probabilities_tensorflow import make_predictions as make_predictions_tensorflow_readm
from combine_los_estimates_tensorflow import make_predictions as make_predictions_tensorflow_los
from readmission_tf_prob_to_likert import convert_to_likert
from create_summary_report import create_report

#get_dataframe_from_apis()
#print('1. Done creating dataframe')
create_structured_data_features()
print('2. Done creating structured data features')
word2vec_all_clean_notes()
print('3. Done cleaning notes word2vec all')
word2vec_all_tokenize_notes()
print('4. Done tokenizing notes word2vec all')
word2vec_all_create_model()
print('5. Done creating model word2vec all')
infected_one_hot()
print('6. Done one-hot-encoding infected keywords with word2vec all model')
clean_readmission_notes()
print('7. Done cleaning notes word2vec readmission')
tokenize_readmission_notes()
print('8. Done tokenizing notes word2vec readmission')
word2vec_readmission_create_model()
print('9. Done creating model word2vec readmission')
readmission_one_hot()
print('10. Done one-hot-encoding readmission keywords with word2vec readmission model')
clean_ner_notes()
print('11. Done cleaning notes NER')
create_file()
print('12. Done creating all note lines file for NER processing')
label_notes()
print('13. Done labeling notes with NER Model')
create_labeled_notes_column()
print('14. Done creating labeled_notes_column')
create_entity_columns()
print('15. Done creating entity columns from the NER-labeled notes')
make_predictions_los_demographics()
print('16. Done creating xgboost model for los demographics')
make_predictions_los_feat()
print('17. Done creating xgboost model for los feature entities')
make_predictions_los_med()
print('18. Done creating xgboost model for los medication entities')
make_predictions_los_neg_feat()
print('19. Done creating xgboost model for los negation feature entities')
make_predictions_los_neg_med()
print('20. Done creating xgboost model for los negation medication entities')
make_predictions_tensorflow_los()
print('21. Done creating tensorflow model for los')
make_predictions_readm_demographics()
print('22. Done creating xgboost model for readmission demographics')
make_predictions_readm_feat()
print('23. Done creating xgboost model for readmission feature entities')
make_predictions_readm_med()
print('24. Done creating xgboost model for readmission medication entities')
make_predictions_readm_neg_feat()
print('25. Done creating xgboost model for readmission negation feature entities')
make_predictions_readm_neg_med()
print('26. Done creating xgboost model for readmission negation medication entities')
make_predictions_tensorflow_readm()
print('27. Done creating tensorflow model for readmission')
convert_to_likert()
print('28. Done converting tensorflow readmission predictions to likert scale')
create_report()
print('29. Done creating summary report')
