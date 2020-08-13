import pandas as pd
from workflow_read_and_write import standard_read_from_db


def create_file():
    df_json_encoded = standard_read_from_db('new_records_ner_cleaned_notes')
    df = pd.read_json(df_json_encoded.decode())
    out_file = open('new_records_all_note_lines.txt','w+')

    for i, row in df.iterrows():
        notes = row['ner_cleaned_notes'].replace(' ##', '')
        print(notes, file=out_file)

