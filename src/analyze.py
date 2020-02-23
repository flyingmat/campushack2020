from typing import List, Set

from raven import *
from nltk import word_tokenize, pos_tag, ne_chunk, Tree
from nltk.tag.stanford import StanfordNERTagger
from nltk.corpus import stopwords
from string import punctuation
import re

english_stop_words = set(stopwords.words('english'))
ner_model = '../stanford-english-corenlp-2018-10-05-models/edu/stanford/nlp/models/ner/english.conll.4class.caseless.distsim.crf.ser.gz'
ner_jar = '../stanford-ner-2018-10-16/stanford-ner.jar'

class TweetData:
    def __init__(self, tweet: Tweet, clean_text: List[str], locations: List[str], sentiment: bool):
        self.tweet = tweet
        self.clean_text = clean_text
        self.locations = locations
        self.sentiment = sentiment

class TweetProcessor:
    def __init__(self, custom_stop_words: Set[str] = set(), deep_clean: bool = True):
        self.ner = StanfordNERTagger(ner_model, ner_jar)
        self.stop_words = english_stop_words.union(custom_stop_words).union(punctuation)
        self.deep_clean = deep_clean

    def clean(self, s: str):
        s = s.lower() # convert text to lower-case
        s = re.sub(r'\n', ' ', s) # replace newline characters

        if self.deep_clean:
            s = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', s) # remove URLs
            s = re.sub('@[^\s]+', '', s) # remove usernames
            s = [c for c in s if c != "#"] # remove the # in #hashtag

        return ''.join(s)

    def ner_clean(self, s: str):
        s = re.sub(r'\n', ' ', s) # replace newline characters
        s = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', s) # replace URLs
        s = re.sub('@[^\s]+', 'USER', s) # replace usernames
        s = [c for c in s if c != "#"] # remove the # in #hashtag
        s = [c for c in s if c not in punctuation]

        return ''.join(s)

    def tokenize(self, s: str):
        return [w for w in word_tokenize(s) if w not in self.stop_words]

    def locations(self, s: str) -> List[str]:
        ssplit = s.split()
        ents = self.ner.tag(ssplit)
        locations = []
        i = 0
        while i < len(ents):
            if (e := ents[i])[1] == 'LOCATION':
                current_comb = [e[0]]
                k = i + 1
                while k < len(ents) and (e2 := ents[k])[1] == 'LOCATION':
                    if ssplit[k-1] == current_comb[-1]:
                        current_comb.append(e2[0])
                    else:
                        break
                    k += 1
                i = k
                locations.append(' '.join(current_comb))
            i += 1
        print(ents)
        return locations

    def get_data(self, tweet: Tweet):
        clean_text = self.clean(tweet.text)
        locations = self.locations(self.ner_clean(tweet.text))
        return TweetData(tweet, self.tokenize(clean_text), locations, True)

if __name__ == '__main__':
    proc = TweetProcessor()
    print(proc.get_data(Tweet(None, "boi i live in the uk lol", None, None)).locations)
    print(proc.get_data(Tweet(None, "i live in Rio de Janeiro", None, None)).locations)
