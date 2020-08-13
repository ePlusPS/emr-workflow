from workflow_read_and_write import standard_read_from_db, lda_output_read_from_db, standard_write_to_db
from nltk import sent_tokenize
import pandas as pd
import re

def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()
    # Break sentence into tokens, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]
    tokens = [token for token in s.split(" ") if len(token)>=3]
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return ["_".join(ngram) for ngram in ngrams]

def create_ngram_tokens(notes):
    new_sentences = sent_tokenize(notes)
    all_ngrams=[]
    for sentence in new_sentences:
        sentence_ngrams=generate_ngrams(sentence, 5)
        all_ngrams+=sentence_ngrams
    ngrams_concat_tokens = [ngram for ngram in all_ngrams]
    return ngrams_concat_tokens

def clean_note(note):
    note = note.replace('\n', '')
    note = note.replace('_', '')
    note = note.replace("|", ' ')
    #note = re.sub(' +', ' ', note)
    #note = re.sub(r'\( (.*) \)', r'(\1)', note)
    #note = re.sub(r' ([,.:])', r'\1', note)
    note = note.replace(' +', ' ')
    note = note.replace('*','')
    note = note.replace('[','')
    note = note.replace(']','')
    note = note.replace('(','')
    note = note.replace(')','')
    note = note.replace('.','')
    note = note.replace(',','')
    note = note.replace(':','')
    note = note.strip()

    return note

def create_lda_ngrams_column(df, lda_topics_list):
    lda_ngrams_column = []
    
    for i, row in df.iterrows():
        note = row['notes']
        cleaned_note = clean_note(note)
        ngrams = create_ngram_tokens(cleaned_note)

        topics_per_row = []
        for lda_topic in lda_topics_list:
            if lda_topic in ngrams:
                topics_per_row.append(lda_topic)

        lda_ngrams_column.append(topics_per_row)
    
    return lda_ngrams_column


def make_lda_topics_list(lda_topics):
    topics_list = []
    for topic in lda_topics:
        substrings = topic[1].split('"')
        for i in range(len(substrings)):
            if i%2 != 0 and substrings[i] not in topics_list:
                topics_list.append(substrings[i])
    return topics_list


def get_ngrams_per_note():
    df_json_encoded = standard_read_from_db('')
    df = pd.read_json(df_json_encoded.decode())

    _, _, lda_topics = lda_output_read_from_db()
    lda_topics_list = make_lda_topics_list(lda_topics)

    lda_ngrams_column = create_lda_ngrams_column(df, lda_topics_list)
    df['lda_ngrams'] = lda_ngrams_column

    df_json_encoded = df.to_json().encode()
    standard_write_to_db('new_records_lda_ngrams_column', df_json_encoded)


