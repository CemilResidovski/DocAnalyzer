import docx2txt
import os
from fnmatch import fnmatch

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

