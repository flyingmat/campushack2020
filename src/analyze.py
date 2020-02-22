import spacy
from raven import *

def locations(s):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(s)
    locations = set([ent for ent in doc.ents if ent.label_=="GPE"])

    return locations

def query_locations(driver, query, n=-1):
    for tweet in tweet_stream(driver, query_to_url(query), n):
        yield tweet, locations(tweet.text)
