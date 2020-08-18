from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import first_table_from_api
import word2vec_prep_clean_notes
import word2vec_prep_tokenize_notes
import create_word2vec_model
import fe_from_readmission_keywords
import fe_from_infection_keywords
import fe_from_structured_readmit_los
import create_lda_model
import combine_dataframes
import run_tpot_los
import run_tpot_readmission
import readmission_word2vec_prep_clean_notes
import readmission_word2vec_prep_tokenize_notes
import create_readmission_word2vec_model
import ner_prep_clean_notes
import make_all_note_lines_file
import inference_per_100000
import add_labeled_notes_column
import create_entity_columns
import readmission_classifier_prep_tokenize_notes
import readmission_classifier_train_and_predict
import xgb_readmission_demographics
import xgb_readmission_feature_entities
import xgb_readmission_medication_entities
import xgb_readmission_neg_feature_entities
import xgb_readmission_neg_medication_entities
import xgb_readmission_lda_topics
import combine_readmission_probabilities_tensorflow
import xgb_los_demographics
import xgb_los_feature_entities
import xgb_los_medication_entities
import xgb_los_neg_feature_entities
import xgb_los_neg_medication_entities
import xgb_los_lda_topics
import combine_los_estimates_tensorflow
import readmission_tf_prob_to_likert
import create_report_summary
import write_summary_report_to_directory
import create_lda_model
import lda_topics_per_note
import readmission_create_lda_model
import readmission_lda_topics_per_note

import placeholder

from datetime import datetime, timedelta

default_args = {
    'owner': 'EMR Appliance Pipeline',
    'start_date': datetime(2020,1,24)
}

dag = DAG('emr-initial-dag', default_args=default_args)

df_from_api_operator = PythonOperator(
    task_id = 'standardize_data_format_from_apis',
    python_callable = first_table_from_api.get_dataframe_from_apis,
    dag = dag
    )

all_word2vec_clean_notes_operator = PythonOperator(
    task_id = 'all_word2vec_prep_clean_notes',
    python_callable = word2vec_prep_clean_notes.clean_all_notes,
    dag = dag
    )

all_word2vec_tokenize_notes_operator = PythonOperator(
    task_id = 'all_word2vec_prep_tokenize_notes',
    python_callable = word2vec_prep_tokenize_notes.tokenize_all_notes,
    dag = dag
    )

all_word2vec_operator = PythonOperator(
    task_id = 'make_all_word2vec_model',
    python_callable = create_word2vec_model.create_word2vec_model,
    dag = dag
    )

readmission_word2vec_clean_notes_operator = PythonOperator(
    task_id = 'readmission_word2vec_prep_clean_notes',
    python_callable = readmission_word2vec_prep_clean_notes.clean_readmission_notes,
    dag = dag
    )

readmission_word2vec_tokenize_notes_operator = PythonOperator(
    task_id = 'readmission_word2vec_tokenize_notes',
    python_callable = readmission_word2vec_prep_tokenize_notes.tokenize_readmission_notes,
    dag = dag
    )

readmission_word2vec_operator = PythonOperator(
    task_id = 'make_readmission_word2vec_model',
    python_callable = create_readmission_word2vec_model.create_word2vec_model,
    dag = dag
    )

label_with_ner_operator = PythonOperator(
    task_id = 'label_notes_with_ner_model',
    python_callable = inference_per_100000.label_notes,
    dag = dag
    )

labeled_notes_column_operator = PythonOperator(
    task_id = 'make_labeled_notes_column',
    python_callable = add_labeled_notes_column.create_labeled_notes_column,
    dag = dag
    )

readmission_one_hot_operator = PythonOperator(
    task_id = 'fe_readmit_one_hot',
    python_callable = fe_from_readmission_keywords.readmission_one_hot,
    dag = dag
    )

infected_one_hot_operator = PythonOperator(
    task_id = 'fe_infected_one_hot',
    python_callable = fe_from_infection_keywords.infected_one_hot,
    dag = dag
    )

structured_features_operator = PythonOperator(
    task_id = 'fe_from_structured_data',
    python_callable = fe_from_structured_readmit_los.create_structured_data_features,
    dag = dag
    )

#combine_all_dataframes_operator = PythonOperator(
#    task_id = 'combine_dataframes_for_tpot',
#    python_callable = combine_dataframes.combine,
#    dag = dag
#    )

#tpot_los_operator = PythonOperator(
#    task_id = 'run_tpot_for_los',
#    python_callable = run_tpot_los.run_tpot,
#    dag = dag
#    )

#tpot_readmission_operator = PythonOperator(
#    task_id = 'run_tpot_for_readmission',
#    python_callable = run_tpot_readmission.run_tpot,
#    dag = dag
#    )

ner_clean_operator = PythonOperator(
    task_id = 'ner_clean_notes',
    python_callable = ner_prep_clean_notes.clean_ner_notes,
    dag = dag
    )

ner_input_text_operator = PythonOperator(
    task_id = 'ner_make_input_text',
    python_callable = make_all_note_lines_file.create_file,
    dag = dag
    )

ner_entity_columns_operator = PythonOperator(
    task_id = 'make_named_entity_columns',
    python_callable = create_entity_columns.create_entity_columns,
    dag = dag
    )

#ner_one_hot_operator = PythonOperator(
#    task_id = 'ner_one_hot',
#    python_callable = placeholder.placeholder_function,
#    dag = dag
#    )

xgb_readmission_demo_operator = PythonOperator(
    task_id = 'readmission_xgb_demographics',
    python_callable = xgb_readmission_demographics.make_predictions,
    dag = dag
    )

xgb_readmission_feat_operator = PythonOperator(
    task_id = 'readmission_xgb_feature_entities',
    python_callable = xgb_readmission_feature_entities.make_predictions,
    dag = dag
    )

xgb_readmission_neg_feat_operator = PythonOperator(
    task_id = 'readmission_xgb_neg_feature_entities',
    python_callable = xgb_readmission_neg_feature_entities.make_predictions,
    dag = dag
    )

xgb_readmission_med_operator = PythonOperator(
    task_id = 'readmission_xgb_medication_entities',
    python_callable = xgb_readmission_medication_entities.make_predictions,
    dag = dag
    )

xgb_readmission_neg_med_operator = PythonOperator(
    task_id = 'readmission_xgb_neg_medication_entities',
    python_callable = xgb_readmission_neg_medication_entities.make_predictions,
    dag = dag
    )

xgb_readmission_lda_operator = PythonOperator(
    task_id = 'readmision_xgb_lda_topics',
    python_callable = xgb_readmission_lda_topics.make_predictions,
    dag = dag)

xgb_los_demo_operator = PythonOperator(
    task_id = 'los_xgb_demographics',
    python_callable = xgb_los_demographics.make_predictions,
    dag = dag
    )

xgb_los_feat_operator = PythonOperator(
    task_id = 'los_xgb_feature_entities',
    python_callable = xgb_los_feature_entities.make_predictions,
    dag = dag
    )

xgb_los_neg_feat_operator = PythonOperator(
    task_id = 'los_xgb_neg_feature_entities',
    python_callable = xgb_los_neg_feature_entities.make_predictions,
    dag = dag
    )

xgb_los_med_operator = PythonOperator(
    task_id = 'los_xgb_medication_entities',
    python_callable = xgb_los_medication_entities.make_predictions,
    dag = dag
    )

xgb_los_neg_med_operator = PythonOperator(
    task_id = 'los_xgb_neg_medication_entities',
    python_callable = xgb_los_neg_medication_entities.make_predictions,
    dag = dag
    )

xgb_los_lda_operator = PythonOperator(
    task_id = 'los_xgb_lda_topics',
    python_callable = xgb_los_lda_topics.make_predictions,
    dag = dag
    )

los_tensorflow_operator = PythonOperator(
    task_id = 'los_tensorflow_model',
    python_callable = combine_los_estimates_tensorflow.make_predictions,
    dag = dag
    )

readmission_tensorflow_operator = PythonOperator(
    task_id = 'readmission_tensorflow_model',
    python_callable = combine_readmission_probabilities_tensorflow.make_predictions,
    dag = dag
    )

readmission_classifier_prep_operator = PythonOperator(
    task_id = 'readmission_classifier_prep_clean',
    python_callable = readmission_classifier_prep_tokenize_notes.readmission_classifier_clean_notes,
    dag = dag
    )

readmission_classifier_train_predict_operator = PythonOperator(
    task_id = 'readmission_classifier_train_predict',
    python_callable = readmission_classifier_train_and_predict.train_and_predict,
    dag = dag
    )

readmission_prob_to_likert_operator = PythonOperator(
    task_id = 'convert_to_likert',
    python_callable = readmission_tf_prob_to_likert.convert_to_likert,
    dag = dag
    )

summary_report_operator = PythonOperator(
    task_id = 'make_summary_report',
    python_callable = create_report_summary.create_report,
    dag = dag
    )

write_to_dash_operator = PythonOperator(
    task_id = 'write_summaries_to_dash',
    python_callable = write_summary_report_to_directory.write_files,
    dag = dag
    )

lda_model_operator = PythonOperator(
    task_id = 'create_lda_model',
    python_callable = create_lda_model.create_lda_model,
    dag = dag
    )

lda_per_note_operator = PythonOperator(
    task_id = 'lda_topics_per_note',
    python_callable = lda_topics_per_note.get_ngrams_per_note,
    dag = dag
    )

readmission_lda_model_operator = PythonOperator(
    task_id = 'readmission_create_lda_model',
    python_callable = readmission_create_lda_model.create_lda_model,
    dag = dag
    )

readmission_lda_topics_per_note_operator = PythonOperator(
    task_id = 'readmission_lda_topics_per_note',
    python_callable = readmission_lda_topics_per_note.get_ngrams_per_note,
    dag = dag
    )

df_from_api_operator.set_downstream(structured_features_operator)
structured_features_operator.set_downstream([
    all_word2vec_clean_notes_operator, 
    readmission_word2vec_clean_notes_operator, 
    ner_clean_operator, 
    readmission_classifier_prep_operator])

readmission_word2vec_clean_notes_operator.set_downstream(readmission_word2vec_tokenize_notes_operator)
readmission_word2vec_tokenize_notes_operator.set_downstream(readmission_word2vec_operator)
readmission_word2vec_operator.set_downstream([readmission_lda_model_operator, readmission_one_hot_operator])
all_word2vec_clean_notes_operator.set_downstream(all_word2vec_tokenize_notes_operator)
all_word2vec_tokenize_notes_operator.set_downstream(all_word2vec_operator)
all_word2vec_operator.set_downstream([infected_one_hot_operator, lda_model_operator])
ner_clean_operator.set_downstream(ner_input_text_operator)
ner_input_text_operator.set_downstream(label_with_ner_operator)
label_with_ner_operator.set_downstream(labeled_notes_column_operator)
labeled_notes_column_operator.set_downstream(ner_entity_columns_operator)
ner_entity_columns_operator.set_downstream([
    xgb_readmission_demo_operator, 
    xgb_readmission_feat_operator,
    xgb_readmission_neg_feat_operator,
    xgb_readmission_med_operator,
    xgb_readmission_neg_med_operator,
    xgb_readmission_lda_operator,
    xgb_los_demo_operator,
    xgb_los_feat_operator,
    xgb_los_neg_feat_operator,
    xgb_los_med_operator,
    xgb_los_neg_med_operator,
    xgb_los_lda_operator])
xgb_los_demo_operator.set_downstream(los_tensorflow_operator)
xgb_los_feat_operator.set_downstream(los_tensorflow_operator)
xgb_los_neg_feat_operator.set_downstream(los_tensorflow_operator)
xgb_los_med_operator.set_downstream(los_tensorflow_operator)
xgb_los_neg_med_operator.set_downstream(los_tensorflow_operator)
xgb_los_lda_operator.set_downstream(los_tensorflow_operator)
readmission_classifier_prep_operator.set_downstream(readmission_classifier_train_predict_operator)
readmission_classifier_train_predict_operator.set_downstream(readmission_tensorflow_operator)
xgb_readmission_demo_operator.set_downstream(readmission_tensorflow_operator)
xgb_readmission_feat_operator.set_downstream(readmission_tensorflow_operator)
xgb_readmission_neg_feat_operator.set_downstream(readmission_tensorflow_operator)
xgb_readmission_med_operator.set_downstream(readmission_tensorflow_operator)
xgb_readmission_neg_med_operator.set_downstream(readmission_tensorflow_operator)
xgb_readmission_lda_operator.set_downstream(readmission_tensorflow_operator)
readmission_tensorflow_operator.set_downstream(readmission_prob_to_likert_operator)
readmission_prob_to_likert_operator.set_downstream(summary_report_operator)
los_tensorflow_operator.set_downstream(summary_report_operator)
lda_model_operator.set_downstream(lda_per_note_operator)
lda_per_note_operator.set_downstream(ner_entity_columns_operator)
readmission_lda_model_operator.set_downstream(readmission_lda_topics_per_note_operator)
readmission_lda_topics_per_note_operator.set_downstream(ner_entity_columns_operator)
summary_report_operator.set_downstream(write_to_dash_operator)
#infected_one_hot_operator.set_downstream(combine_all_dataframes_operator)
#readmission_one_hot_operator.set_downstream(combine_all_dataframes_operator)
#combine_all_dataframes_operator.set_downstream([tpot_los_operator, tpot_readmission_operator])

