import re
import numpy as np
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import dill as pickle


def identity_tokenizer(text):
    return text


le = pickle.load(open('model/encoder.sav', 'rb')) # loading label encoder
clf = pickle.load(open('model/model.sav', 'rb')) # loading logistic regression classifier
tfidf = pickle.load(open('model/tfidf.sav', 'rb')) # loading TFIDF vectorizer
stop_words = ['start', 'purchase', 'worth', 'Rs', 'rs', 'Rs.', 'rs.'] # nouns to be ignored


def extract_amount(X):
    r = re.compile('[0-9,]+')  # extract numbers from text
    return re.findall(r, X)


def extract_nouns(X):
    is_noun = lambda pos: pos[:2] == 'NN' # pos tags for noun
    X = preprocess(X) # invoking preprocess
    # print(pos_tag(X))
    nouns = [word for (word, pos) in pos_tag(X) if is_noun(pos)] # filtering nouns
    nouns = [noun for noun in nouns if noun not in stop_words] # removing stop wordsd

    return nouns
    # return ' '.join(nouns)


def preprocess(X):
    # X = X.lower()
    r = re.compile('[0-9]+') # regex for numbers
    X = re.sub(r, '', X) # removing numbers from text
    X = ''.join(c for c in X if c not in punctuation) # removing function and joining words

    stopword = stopwords.words('english') # stop words in English
    wordnet_lemmatizer = WordNetLemmatizer() # Wordnet Lemmatizer
    X = word_tokenize(X) # tokenizing into words
    X = [wordnet_lemmatizer.lemmatize(x, 'v') for x in X]
    X = [word for word in X if word not in stopword] # removing stop words

    return X


def predict(test):
    X = preprocess(test) # preprocessing text
    X = [X] # creating as array
    X = tfidf.transform(X) # tfidf features
    X = np.asarray(X.todense()) # converting into Numpy array
    y = clf.predict(X) # predicting the class
    y = le.inverse_transform(y) # taking inverse transform to get the class name

    return y