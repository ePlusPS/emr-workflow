from workflow_read_and_write import standard_write_to_db
import pandas as pd

def get_records():
    #have to figure out how to get the records that will be inferenced upon.
    #these records will be in the same format as first_dataframe collection.
    
    new_records_df = pd.DataFrame()
    new_records_df_json_encoded = new_records_df.to_json().encoded()

    standard_write_to_db('new_records', new_records_df_json_encoded)

