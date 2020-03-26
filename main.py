from AnalyzeDocument import AnalyzeDocument
from pathlib import Path

path = Path('C:/Users/cemil/Desktop')
file = path / 'Recommended_SDV_settings.docx'

document = AnalyzeDocument(file)
print(document)