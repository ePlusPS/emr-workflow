from workflow_read_and_write import readmission_classifier_read_from_db, xgb_read_from_db, standard_write_to_db
import pandas as pd
import datetime

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def create_model(proba_df, labels):
    model = Sequential()
    model.add(Dense(20,input_shape=[len(proba_df.columns)], activation = 'relu'))
    model.add(Dense(20, activation = 'relu'))
    model.add(Dense(1, activation = 'sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer = 'Adam', metrics = ['acc'])
    model.fit(proba_df, labels, epochs=15)

    return model

def predict_with_model(proba_df, model):
    predictions = model.predict(proba_df)
    return predictions

def make_predictions():
    readmission_classifier_df_json_encoded, _  = readmission_classifier_read_from_db()
    readmission_classifier_df = pd.read_json(readmission_classifier_df_json_encoded.decode())

    xgb_demo_df_json_encoded, top_n_demo_df_json_encoded, _ = xgb_read_from_db('demo_xgb_readmission')
    xgb_demo_df = pd.read_json(xgb_demo_df_json_encoded.decode())
    top_n_demo_df = pd.read_json(top_n_demo_df_json_encoded.decode())

    xgb_feat_df_json_encoded, top_n_feat_df_json_encoded, _ = xgb_read_from_db('feat_xgb_readmission')
    xgb_feat_df = pd.read_json(xgb_feat_df_json_encoded.decode())
    top_n_feat_df = pd.read_json(top_n_feat_df_json_encoded.decode())

    xgb_neg_feat_df_json_encoded, top_n_neg_feat_df_json_encoded, _ = xgb_read_from_db('neg_feat_xgb_readmission')
    xgb_neg_feat_df = pd.read_json(xgb_feat_df_json_encoded.decode())
    top_n_neg_feat_df = pd.read_json(top_n_neg_feat_df_json_encoded.decode())

    xgb_med_df_json_encoded, top_n_med_df_json_encoded, _ = xgb_read_from_db('med_xgb_readmission')
    xgb_med_df = pd.read_json(xgb_med_df_json_encoded.decode())
    top_n_med_df = pd.read_json(top_n_med_df_json_encoded.decode())

    xgb_neg_med_df_json_encoded, top_n_neg_med_df_json_encoded, _ = xgb_read_from_db('neg_med_xgb_readmission')
    xgb_neg_med_df = pd.read_json(xgb_neg_med_df_json_encoded.decode())
    top_n_neg_med_df = pd.read_json(top_n_neg_med_df_json_encoded.decode())

    xgb_lda_df_json_encoded, top_n_lda_df_json_encoded, _ = xgb_read_from_db('lda_xgb_readmission')
    xgb_lda_df = pd.read_json(xgb_lda_df_json_encoded.decode())
    top_n_lda_df = pd.read_json(top_n_lda_df_json_encoded.decode())

    prev_probas = pd.DataFrame()
    prev_probas['readmission_classifier_probabilities'] = readmission_classifier_df['readmission_classifier_probabilities']
    prev_probas['xgb_demo_ent_pred'] = xgb_demo_df['xgb_demo_ent_pred']
    prev_probas['xgb_feat_ent_pred'] = xgb_feat_df['xgb_feat_ent_pred']
    prev_probas['xgb_neg_feat_ent_pred'] =  xgb_neg_feat_df['xgb_feat_ent_pred']
    prev_probas['xgb_med_ent_pred'] = xgb_med_df['xgb_med_ent_pred']
    prev_probas['xgb_neg_med_ent_pred'] = xgb_med_df['xgb_med_ent_pred']
    prev_probas['xgb_lda_pred'] = xgb_lda_df['xgb_lda_pred']

    tf_input = pd.concat(
            [#prev_probas, 
            top_n_demo_df, 
            top_n_feat_df, 
            top_n_neg_feat_df, 
            top_n_med_df, 
            top_n_neg_med_df,
            top_n_lda_df], axis=1)

    print('prev_probas: '+prev_probas.columns)
    print('top_n_demo_df: '+top_n_demo_df.columns)
    print('top_n_feat_df: '+top_n_feat_df.columns)
    print('top_n_neg_feat_df: '+top_n_neg_feat_df.columns)
    print('top_n_med_df: '+top_n_med_df.columns)
    print('top_n_neg_med_df: '+top_n_neg_med_df.columns)

    print(tf_input.columns)
    readmissions = xgb_demo_df['readmission']

    model = create_model(tf_input, readmissions)
    model_predictions = predict_with_model(tf_input, model)
    tf_input['keras_pred'] = model_predictions

    tf_input_json_encoded = tf_input.to_json().encode()
    standard_write_to_db('readmission_tensorflow_predictions', tf_input_json_encoded)

    now = datetime.datetime.now()
    str_datetime =now.strftime("%m-%d-%Y_%H:%M:%S")
    model.save('tf_readmission/most_recent')
    model.save('tf_readmission/'+str_datetime)
