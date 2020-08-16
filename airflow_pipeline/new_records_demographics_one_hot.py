from workflow_read_and_write import standard_read_from_db, standard_write_to_db
import pandas as pd
from sklearn.preprocessing import LabelBinarizer


def make_one_hot(df):

    gender_one_hot = pd.DataFrame()
    gender_one_hot['Male'] = (df['gender'] == 'M').astype(float)
    gender_one_hot['Female'] = (df['gender'] == 'F').astype(float)

    lb = LabelBinarizer()
    ethnicity = df['ethnicity']
    eth_df = (pd.DataFrame(lb.fit_transform(ethnicity), columns=lb.classes_,index=df.index))

    lb = LabelBinarizer()
    insurance = df['insurance']
    ins_df = (pd.DataFrame(lb.fit_transform(insurance), columns=lb.classes_,index=df.index))

    combined = pd.concat([gender_one_hot, eth_df, ins_df], axis=1)

    demo_one_hot = pd.DataFrame()
    for column in combined.columns:
        new_column = column
        if '[' in new_column:
            new_column = new_column.replace('[', '')
        if ']' in new_column:
            new_column = new_column.replace(']', '')
        if ',' in new_column:
            new_column = new_column.replace(',', '_')
        if ' ' in new_column:
            new_column = new_column.replace(' ', '_')
        demo_one_hot[new_column] = combined[column]

    return demo_one_hot

def new_records_demo_one_hot():
    df_json_encoded = standard_read_from_db('new_records')
    df = pd.read_json(df_json_encoded.decode())

    demo_one_hot = make_one_hot(df)
    
    demo_one_hot_json_encoded = demo_one_hot.to_json().encode()
    standard_write_to_db('new_records_demographics')

