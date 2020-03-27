import docx2txt
import os
from fnmatch import fnmatch
from pathlib import Path
import json
import string
import nltk
# nltk.download('crubadan')
# nltk.download('punkt')
from nltk.classify.textcat import TextCat
from nltk.corpus import wordnet, stopwords
from nltk.stem import SnowballStemmer

def get_wordnet_pos(token):
    """Map POS tag to first character lemmatize() accepts"""
    pos_tag = nltk.pos_tag([token])[0][1][0].upper()
    pos_tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

    return pos_tag_dict[pos_tag]

def get_stem_language(language):
    """Map language to form stem() accepts"""
    # extend as needed
    language_dict = {"eng": "english",
                     "swe": "swedish",
                     "ger": "german"}
    
    return language_dict[language]

    
class AnalyzeDocument():
    """Class for analyzing text documents"""
    def __init__(self, indata):
        if os.path.isfile(indata):
            if fnmatch(str(indata).lower().split('.')[-1], 'doc*'):
                self.body = docx2txt.process(indata)
        else:
            self.body = indata
        
    def word_tokenize(self):
        """Return the text without punctuation characters or upper case letters"""
        text = self.body.lower()
        # Translate punctuation chars (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~) into nothing, removing from string
        return text.translate(str.maketrans('', '', string.punctuation)).split()
    
    def language(self):
        """Return identified language of the text"""
        tc = TextCat()
        return tc.guess_language(self.body)

    def word_count(self):
        """Return the number of words in the text"""
        return len(self.word_tokenize())

    def unique_word_count(self):
        """Return the number of unique words in the text"""
        return len(set(self.word_tokenize()))

    def pos_dictionary(self, friendly=False):
        """Return dictionary of part-of-speech tags in the text, optionally return tags with friendly names"""
        # Get pos tags for each token 
        pos = nltk.pos_tag(self.word_tokenize(), lang=self.language())
        
        if friendly:
            with open('pos_tags_explanations.json', mode='r') as pos_tags_explanations_json:
                pos_tags_explanations = json.load(pos_tags_explanations_json)
            pos_dict = {token: pos_tags_explanations[pos_tag]  for token, pos_tag in pos}
        else:
            pos_dict = {token: pos_tag for token, pos_tag in pos}
        
        return pos_dict
        
    def pos_count_dictionary(self):
        """Return dictionary of part-of-speech tag count in the text"""
        pos_tag_set = set(self.pos_dictionary().values())
        pos_count_dict = {}
        
        for pos_tag in pos_tag_set:
            pos_count_dict[pos_tag] = list(self.pos_dictionary().values()).count(pos_tag)

        return pos_count_dict
        
    def word_count_dictionary(self):
        """Return dictionary of word count in the text"""
        tokens = self.word_tokenize()
        count_dict = {word: tokens.count(word) for word in tokens}
        count_dict_sorted = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))
        
        return count_dict_sorted
    
    def lemmatize(self):
        """Return list of lemmatized words. Support only for English or Russian."""
        wnl = nltk.WordNetLemmatizer()
        lemmas = []
        
        for token in self.word_tokenize():
            pos_tag = get_wordnet_pos(self.pos_dictionary()[token])
            lemmas.append(wnl.lemmatize(token, pos_tag))
        
        return lemmas
    
    def lemma_count(self):
        lemmas = self.lemmatize()
        return len(set(lemmas))

    def stem(self):
        stemmer = SnowballStemmer(get_stem_language(self.language()))
        stems = []
        
        for token in self.word_tokenize():
            stems.append(stemmer.stem(token))
        
        return stems

    def __repr__(self):
        return 'class AnalyzeDocument(indata=str)'

    def __str__(self):
        return self.body