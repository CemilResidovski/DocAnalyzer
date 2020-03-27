import docx2txt
import os
from fnmatch import fnmatch
from pathlib import Path
import json
import string
import nltk
from nltk.classify.textcat import TextCat
from nltk.corpus import wordnet, stopwords

def get_wordnet_pos(token):
    """Map POS tag to first character lemmatize() accepts"""
    pos_tag = nltk.pos_tag([token])[0][1][0].upper()
    pos_tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

    return pos_tag_dict[pos_tag]

class AnalyzeDocument():
    """Class for analyzing text documents"""
    def __init__(self, indata):
        if os.path.isfile(indata):
            if fnmatch(str(indata).lower().split('.')[-1], 'doc*'):
                self.body = docx2txt.process(indata)
        else:
            self.body = indata
        
    def word_tokenize(self):
        text = self.body.lower()
        # Translate punctuation chars (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~) into nothing, removing from string
        tokens = text.translate(str.maketrans('', '', string.punctuation)).split()
        
        return tokens
    
    def language(self):
        tc = TextCat()
        language = tc.guess_language(self.body)
        
        return language

    def word_count(self, unique=True):
        # set(tokens) creates a set with only the unique words
        tokens = self.word_tokenize()
        
        if not unique:
            return len(tokens)
        
        return len(set(tokens))

    def pos_dictionary(self, friendly=False, count=False):
        pos = nltk.pos_tag(self.word_tokenize(), lang=self.language())
        
        if friendly:
            with open('pos_tags_explanations.json', mode='r') as pos_tags_explanations_json:
                pos_tags_explanations = json.load(pos_tags_explanations_json)
            pos_dict = {token: pos_tags_explanations[pos_tag]  for token, pos_tag in pos}
        else:
            pos_dict = {token: pos_tag for token, pos_tag in pos}
        
        pos_tag_set = set(pos_dict.values())
        pos_count_dict = {pos_tag: list(pos_dict.values()).count(pos_tag) for pos_tag in pos_tag_set}
        
        if count:
            return pos_count_dict
        
        return pos_dict

    def word_count_dictionary(self):
        tokens = self.word_tokenize()
        count_dict = {word: tokens.count(word) for word in tokens}
        count_dict_sorted = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))
        
        return count_dict_sorted
    
    def lemmatize(self):
        wnl = nltk.WordNetLemmatizer()
        lemmas = []
        
        for token in self.word_tokenize():
            pos_tag = get_wordnet_pos(self.pos_dictionary()[token])
            lemmas.append(wnl.lemmatize(token, pos_tag))
        
        return lemmas
    
    def __repr__(self):
        return 'class AnalyzeDocument(indata=str)'

    def __str__(self):
        return self.body