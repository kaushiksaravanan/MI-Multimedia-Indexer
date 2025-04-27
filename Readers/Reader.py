from email.mime import audio
import os.path
from Readers.audio import voice_text as audioReader

try:
    from Readers.doc import read_doc as readDocWithImage
except:
    print("easyocr not found")

from Readers.FileReader import *

try:
    from Readers.pdf import read_pdf as readPdf
except:
    print("easyocr not found")

try:
    from Readers.read_image import read_image as readImageEasy
except:
    print("easyocr not found")

from Readers.readDoc import readDoc
extension = lambda filename : os.path.splitext(filename)[1]

def readFile(path):

    ext = extension(path)
    # print(ext, path)

    try:

        if ext in [".txt", ".csv", ".json", ".yaml", ".xml", ".md", ".js", ".css", ".html", ".cpp"]:
            return readHumanReadableText(path)

        elif exit == ".pdf":
            return readPdf(path)

        elif ext in [".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".jpg", ".eps", ".raw", ".cr2", ".nef", ".orf", ".sr2"]:
            # print("Skipping image")
            # return ""
            return " ".join(readImageEasy(path))

        elif ext in [".xlsx",".xlsm",".xltx",".xltm"]:
            return readSpreadSheet(path)

        elif ext in [".doc", ".docx"]:
            try:
                return readDoc(path)
            except:
                return readDocWithImage(path)

        elif ext in [".wav", ".mp3"]:
            return audioReader(path)

        else:
            print("{} not read".format(ext))
            return ""

    except:
        print("Unable to read : {}".format(path))
        return ""

