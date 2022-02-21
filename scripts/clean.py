# this script contains the functions for cleaning and prepping the datasets for making recommendations

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import numpy as np
import re

import nltk
nltk.download('punkt')
nltk.download('wordnet')


# defining the functions

def clean_prep_data(data):
    '''
    returns clean dataframe that can be used to make recommendations

    INPUTS:
    data - the dataset obtained from scrape.scrape

    OUTPUTS:
    df - a clean dataframe

    '''
    df = data

    if 'Unnamed: 0' in df.columns:
        del df['Unnamed: 0']

    # creating id column
    df['id'] = range(1, df.shape[0] + 1)
    df = pd.concat([df['id'], df.iloc[:, :-1]], axis= 1)

    # removing internship profiles if 'no company found' in df
    drop_index = df[df.start == 'no company found'].index
    df.drop(drop_index, axis=0)

    # removing unnecessary spaces and characters
    df.iloc[:,1:] = df.iloc[:,1:].apply(lambda x: x.str.replace('\t', ' ')).apply(lambda x: x.str.replace('\n', ' ')).apply(lambda x: x.str.replace('\r',' '))
    df.iloc[:,1:] = df.iloc[:,1:].apply(lambda x: x.str.strip())
    df.iloc[:,1:] = df.iloc[:,1:].apply(lambda x: x.str.replace('\s{2}', ' '))
    df.iloc[:,1:] = df.iloc[:,1:].apply(lambda x: x.str.replace('\xa0', ''))
    df['skills'] = df.skills.str.replace('Skills Required', '')
    df = pd.concat([df.id,df.iloc[:, 2:].apply(lambda x: x.str.lower()), df.href], axis = 1)

    # working with dates
    df.start = pd.to_datetime(df.start, errors = 'coerce')
    df.end = pd.to_datetime(df.end, errors='coerce')

    # compensation column to be converted to 2 categories
    compensation_dict = {'recurring': 'paid', 'one-time': 'paid', 'paid (monthly, variable)':'paid', 
                         'expenses covered': 'paid', 'unpaid': 'unpaid'}
    df.compensation = df.compensation.map(compensation_dict)

    # working with skills and job_loc
    df.skills = df.skills.str.replace('(?<=\S)\s{2,}', ',', regex= True)
    df.job_loc = df.job_loc.str.replace('(?<=\S)\s{2,}', '', regex = True)

    # working with details column
    df.details = df.details.str.replace('about internship:', '')
    df.details = df.details.str.replace('roles and responsibilities:', '')
    df.details = df.details.str.split('skill', expand=True)[0]
    df.details = df.details.str.split('perks', expand=True)[0]

    # removing duplicates
    df.sort_values(by='start', ascending= False, inplace =True)
    df.drop_duplicates(subset = ['job_title', 'company_name', 'job_loc','category'],keep='first',inplace = True)

    # drop those rows that have at least 10 non NA values
    df.dropna(thresh=10, inplace= True)
    
    return df

def tokenize(sentences):
    '''
    tokenizes a bunch of sentences after normalizing them and returns stemmed tokens.

    INPUT:
    sentences - a paragraph that need to be tokenized

    OUTPUT:
    tokens - list of stemmed tokens

    '''
    # normalizing, tokenizing, lemmatizing
    sentences = re.sub('\W', ' ', sentences) 
    sentences = re.sub('[0-9]', ' ', sentences)

    tokens = word_tokenize(sentences)
    tokens = [i.strip() for i in tokens]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(i) for i in tokens]
    return tokens


def similarity_matrix_wo_tfidf(df):
    '''
    returns a similarity matrix, in the form of a dataframe, between different internships by using the 
    details section

    INPUT:
    df - dataframe with 'details' as one of the columns

    OUTPUT:
    sim - similarity matrix(dataframe) with internship id as column and row labels 

    '''
    details = df['details']
    vect = CountVectorizer(tokenizer=tokenize, stop_words= 'english')

    mat = vect.fit_transform(details).toarray()
    sim = np.dot(mat, mat.T)
    sim = pd.DataFrame(sim, columns=df.id, index=df.id)
    return sim


def similarity_matrix_cat(df):
    '''
    returns a similarity matrix, in the form of a dataframe, between different internships by using the 
    cat section

    INPUT:
    df - dataframe with 'category' as one of the columns

    OUTPUT:
    sim - similarity matrix(dataframe) with internship id as column and row labels 
    '''
    cats = df['category']
    vect = CountVectorizer(tokenizer=tokenize, stop_words= 'english')
    tfidf = TfidfTransformer()

    mat = vect.fit_transform(cats).toarray()
    sim = np.dot(mat, mat.T)
    sim = pd.DataFrame(sim, columns=df.id, index=df.id)
    return sim

def return_sim(df):
    '''
    returns similarity dataframe and accepts clean dataframe
    '''
    sim_1 = similarity_matrix_wo_tfidf(df)
    sim_cat = similarity_matrix_cat(df)
    sim = sim_1 * 0.3 + sim_cat

    return sim







