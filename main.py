from AnalyzeDocument import AnalyzeDocument
from pathlib import Path

string = r'C:\Users\drilo\Vimur AB\Vimur - Documents\Kunder och sälj\_Säljmaterial\Inphinity'
path = Path(string.replace('\\', '/'))
file = path / 'Inphinity Forms Tutorial.docx'

document = AnalyzeDocument(file)
print(document)