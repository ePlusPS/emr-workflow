from workflow_read_and_write import standard_read_from_db, xgb_read_from_db, standard_write_to_db
import pandas as pd

def make_tf_columns(df, top_n_col_dict, ner_entity_df, lda_topics_df, demo_one_hot_df):
    
    top_n_demo_df = pd.DataFrame()
    for col in top_n_col_dict['demo']:
        top_n_demo_df[col] = demo_one_hot_df[col]

    top_n_feat_df = pd.DataFrame()
    for col in top_n_col_dict['feat']:
        binary_col = []
        for i, row in ner_entity_df.iterrows():
            val = col in row['feature_entities']
            binary_col.append(val)
        top_n_feat_df[col] = binary_col

    top_n_neg_feat_df = pd.DataFrame()
    for col in top_n_col_dict['neg_feat']:
        binary_col = []
        for i, row in ner_entity_df.iterrows():
            val = col in row['neg_feature_entities']
            binary_col.append(val)
        top_n_neg_feat_df[col] = binary_col

    top_n_med_df = pd.DataFrame()
    for col in top_n_col_dict['med']:
        binary_col = []
        for i, row in ner_entity_df.iterrows():
            val = col in row['medication_entities']
            binary_col.append(val)
        top_n_med_df[col] = binary_col

    top_n_neg_med_df = pd.DataFrame()
    for col in top_n_col_dict['neg_med']:
        binary_col = []
        for i, row in ner_entity_df.iterrows():
            val = col in row['neg_medication_entities']
            binary_col.append(val)
        top_n_neg_med_df[col] = binary_col

    top_n_lda_df = pd.DataFrame()
    for col in top_n_col_dict['lda']:
        binary_col = []
        for i, row in lda_topics_df:
            val = col in row['lda_ngrams']
            binary_col.append(val)
        top_n_lda_df[col] = binary_col

    tf_input = pd.concat(
            [top_n_demo_df,
            top_n_feat_df,
            top_n_neg_feat_df,
            top_n_med_df,
            top_n_neg_med_df,
            top_n_lda_df], axis=1)

    return tf_input

def make_input():
    _, top_n_feat_df_json_encoded, _ = xgb_read_from_db('feat_xgb_readmission')
    top_n_feat_df = pd.read_json(top_n_feat_df_json_encoded.decode())

    _, top_n_neg_feat_df_json_encoded, _ = xgb_read_from_db('neg_feat_xgb_readmission')
    top_n_neg_feat_df = pd.read_json(top_n_neg_feat_df.decode())

    _, top_n_med_df_json_encoded, _ = xgb_read_from_db('med_xgb_readmission')
    top_n_med_df = pd.read_json(top_n_med_df_json_encoded.decode())

    _, top_n_neg_med_df_json_encoded, _ = xgb_read_from_db('neg_med_xgb_readmission')
    top_n_neg_med_df = pd.read_json(top_n_neg_med_df_json_encoded.decode())

    _, top_n_lda_df_json_encoded, _ = xgb_read_from_db('lda_xgb_readmission')
    top_n_lda_df = pd.read_json(top_n_lda_df_json_encoded.decode())

    _, top_n_demo_df_json_encoded, _ = xgb_read_from_db('demo_xgb_readmission')
    top_n_demo_df = pd.read_json(top_n_demo_df_json_encoded.decode())

    top_n_dict = {}
    top_n_dict['feat'] = top_n_feat_df.columns
    top_n_dict['neg_feat'] = top_n_neg_feat_df.columns
    top_n_dict['med'] = top_n_med_df.columns
    top_n_dict['neg_med'] = top_n_neg_med_df.columns
    top_n_dict['lda'] = top_n_lda_df.columns
    top_n_dict['demo'] = top_n_demo_df.columns

    records_df_json_encoded = standard_read_from_db('new_records')
    records_df = pd.read_json(records_df_json_encoded.decode())

    # retrieve demo_one_hot_df, lda_topics_df, and entity_columns_df
    ner_entity_df_json_encoded = standard_read_from_db('new_records_entity_columns')
    ner_entity_df = pd.read_json(ner_entity_df_json_encoded.decode())

    lda_topics_df_json_encoded = standard_read_from_db('new_records_lda_ngrams_column')
    lda_topics_df = pd.read_json(lda_topics_df_json_encoded.decode())

    demo_one_hot_df_json_encoded = standard_read_from_db('new_records_demographics')
    demo_one_hot_df = pd.read_json(demo_one_hot_df_json_encoded.decode())

    tf_input = make_tf_columns(records_df, top_n_dict, ner_entity_df, lda_topics_df, demo_one_hot_df)

    tf_input_json_encoded = tf_input.to_json().encode()
    standard_write_to_db('new_records_readmission_tf_input', tf_input_json_encoded)

