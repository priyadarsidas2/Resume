import aspose.words as aw
import random

def extractTextFromPDF(filename):
    # Load the PDF document from the disc.
    doc = aw.Document(filename)

    # Save the document to HTML format.
    fileNameToSave = "output/" + "filename" + str(random.randint(0,10000)) + ".html"
    doc.save(fileNameToSave)
    doc = aw.Document(fileNameToSave)
    from bs4 import BeautifulSoup

    with open(fileNameToSave, encoding="utf8") as f:
        #read File
        content = f.read()
        #parse HTML
        soup = BeautifulSoup(content, 'html.parser')

    extractedText = ""
    for i in soup.find_all('p'):
        extractedText += "\n" + i.get_text()

    return extractedText
