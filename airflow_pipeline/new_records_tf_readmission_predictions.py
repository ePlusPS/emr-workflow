from workflow_read_and_write import standard_read_from_db, standard_write_to_db
from tensorflow import keras
import pandas as pd

def predict_with_model(tf_input, tf_model):
    predictions = tf_model.predict(tf_input)
    return predictions

def make_tf_predictions():
    tf_input_df_json_encoded = standard_read_from_db('new_records_readmission_tf_input')
    tf_input_df = pd.read_json(tf_input_df_json_encoded.decode())
    
    model = keras.models.load_model('tf_readmission/most_recent')

    predictions = predict_with_model(tf_input_df, model)
    tf_input_df['tf_readmission_pred'] = predictions

    tf_input_json_encoded = tf_input_df.to_json().encode()
    standard_write_to_db('new_records_readmission_tf_predictions', tf_input_json_encoded)

