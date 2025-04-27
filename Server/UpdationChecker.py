import os, Server.orm
exclude = [".git",".ipynb_checkpoints", "__pycache__", "Tesseract-OCR"]
from Readers.Reader import readFile
from Preprocessing.RemoveStopWords import remove_stopwords
from Server.orm import lastmodified, db, engine, getAll, File
import warnings

warnings.filterwarnings("ignore")
db.metadata.create_all(engine)

def getAllFiles(path = os.path.join(os.getcwd(), "SampleFiles")):
    listOfFiles = []
    files = [k for k in [os.path.join(path, f) for f in os.listdir(path) if f != "IndexingData.json"] if os.path.isfile(k)]
    listOfFiles += files
    subdirs = [k for k in [os.path.join(path, f) for f in os.listdir(path) if f not in exclude] if os.path.isdir(k)]

    for i in subdirs:
        listOfFiles += getAllFiles(i)
    
    return listOfFiles

def getLastModified(path):
    return os.path.getmtime(path)

def updateChecker(path = os.path.join(os.getcwd(), "SampleFiles")):
    previous_version = {}
    for i in getAll():
        previous_version[i] = lastmodified(cleanPath(i))
    # print(previous_version)
    new_files = set(getAllFiles(path))
    old_files = set(tuple(previous_version.keys()))
        
    files_added = [cleanPath(i) for i in list(new_files - old_files)]
    files_deleted = [cleanPath(i) for i in list(old_files - new_files)]
    files_modified = []

    for i in (new_files & old_files):
        if previous_version[i] != getLastModified(str(i)):
            files_modified.append(cleanPath(str(i)))

    return {
        "added" : files_added,
        "deleted" : files_deleted,
        "modified" : files_modified
    }

def cleanPath(i):
    if type(i) == str:
        return i
    elif type(i) == File:
        return i.path


# if __name__ == "__main__":
#     print(lastmodified())
    # d = updateChecker("SampleFiles")
    # for i in d:
    #     print(i)
    #     print(d[i])
    #     print()
    # for i in getAllFiles():
    #     s = readFile(i)
    #     print(s)
    #     print()
    #     print(remove_stopwords(s))
    #     print("---------------")
    #     print()