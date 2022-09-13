import PyPDF2

def readpdffile(fileName):
    pdfFileObj = open(fileName, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # printing number of pages in pdf file
    print(pdfReader.numPages)

    extractedText = ''
    for i in range(pdfReader.numPages):
        # creating a page object
        pageObj = pdfReader.getPage(i)
        # extracting text from page
        localText = pageObj.extractText()
        extractedText += localText
    return extractedText
