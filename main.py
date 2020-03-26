from AnalyzeDocument import AnalyzeDocument
from pathlib import Path

string = 'C:\Users\drilo\Vimur AB\Vimur - Documents\Kunder och sälj\_Säljmaterial\Inphinity'
path = Path(string.replace('\', '/'))
file = path / 'Recommended_SDV_settings.docx'

document = AnalyzeDocument(file)
print(document)