import pandas as pd
from workflow_read_and_write import summary_report_read_from_db

def write_files():
    pat_df_json_encoded, hosp_df_json_encoded = summary_report_read_from_db()
    
    pat_df = pd.read_json(pat_df_json_encoded.decode())
    hosp_df = pd.read_json(hosp_df_json_encoded.decode())

    pat_df.to_csv('/home/ubuntu/emr-workflow/dashapp/data/patient_summary.csv')
    hosp_df.to_csv('/home/ubuntu/emr-workflow/dashapp/data/hospital_summary.csv')
