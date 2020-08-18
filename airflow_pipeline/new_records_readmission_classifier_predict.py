from workflow_read_and_write import standard_read_from_db, readmission_classifier_write_to_db
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
import pickle

def create_dataset(df):
    tfidfconverter = TfidfVectorizer(max_features=5000, strip_accents='unicode', decode_error = 'ignore', stop_words = stopwords.words('english'))
    X = tfidfconverter.fit_transform(df['readmission_classifier_tokens'].to_list()).toarray()
    y = df['readmission'].to_numpy()
    
    # We're not using the splitting of the data currently. Since we only want the raw probabilities,
    # I have the classifier fitting to the whole dataset.
    #train_test_split.stratify = True
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 0, stratify = y)

    return X, y


def make_probability_column(classifier, input_features):
    y_hat = classifier.predict_proba(input_features)[:,1]
    return y_hat
    
def predict():
    df_json_encoded = standard_read_from_db('new_records_readmission_classifier_tokens')
    df = pd.read_json(df_json_encoded.decode())
    
    X, y = create_dataset(df)

    _, classifier_pickle = readmission_classifier_read_from_db()
    classifier = pickle.loads(classifier)

    probabilities = make_probability_column(classifier, X)
    df['readmission_classifier_probabilities'] = probabilities

    df_json_encoded = df.to_json().encode()

    standard_write_to_db('new_records_readmission_classifier_pred', df_json_encoded)
