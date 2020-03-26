import docx2txt
import os
from fnmatch import fnmatch
import string

class AnalyzeDocument():

    def __init__(self, indata):
        if os.path.isfile(indata):
            if fnmatch(str(indata).lower().split('.')[-1], 'doc*'):
                self.body = docx2txt.process(indata)
        else:
            self.body = indata
            
    def __repr__(self):
        return 'class Document(indata=str)'

    def __str__(self):
        return self.body

    def word_count(self, unique=True):
        text = self.body.lower()
        # Translate punctuation chars (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~) into nothing, removing from string
        # set(cleaned) creates a set with only the unique letters
        cleaned = text.translate(str.maketrans('', '', string.punctuation)).split()
        if not unique:
            return len(cleaned)
            
        return len(set(cleaned))