import time
import os
import threading
from datetime import datetime
import json
from turtle import down
import schedule # type: ignore
import time
from json import loads
import warnings
from SQLReader.SQLReader import getAllData, getAllTables, getDataByTable
warnings.filterwarnings("ignore")

# from Server.Server import db
from Server.Server import intKeys, app
from Server.WatchDog import OnMyWatch, setAnyModified, getAnyModified
from Server.orm import getAll, init_db, select_all_files, session, insert_file, delete_file, update_file
from Server.UpdationChecker import updateChecker, getLastModified, getAllFiles
from Readers.Reader import readFile

from Preprocessing.RemoveStopWords import remove_stopwords
from Preprocessing.Tokenization import tokenizer, newTokenizer
from Preprocessing.RuleMining import RuleMiner, newRuleMiner

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# db.create_all()

path = "D:\\SmartIndiaHackathon2022\\SampleFiles"
print("cwd",path)

class myThread (threading.Thread):
    def __init__(self, threadID, func, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.func = func
        self.args = args

    def run(self):
        print("Starting " + self.threadID)
        self.func(*self.args)
        print("Exiting " + self.threadID)

def run_server(threadName, port = 5678):
    print(threadName, port)
    print("Started the Thread : {}".format(threadName))
    app.run(port=port)

def run_watch_dog(threadName, src):
    print(threadName, src)
    watch = OnMyWatch(src)
    print("Started the Thread : {}".format(threadName))
    watch.run()

# def init_reading():
#     files = getAllFiles(path)
#     content = {i:"" for i in files}
#     # print("Files Found :")
#     # print(*files, sep="\n")
#     # print("-"*50)
#     arr = []

#     for i in files:
#         content[i] = remove_stopwords(readFile(i))# + " " + " ".join(i.split("\\")))
#         arr.append(content[i])

#     for i in getAllData():
#         arr.append(remove_stopwords(i))

#     tokenizer.text_tokenizer(arr)
#     # print(tokenizer.word_index)

#     for i in content:
#         content[i] = {
#             "path" : i,
#             "data" : content[i],
#             "last_modified" : getLastModified(i),
#             "tokens" : tokenizer.tokenize_given_string(content[i])
#         }

#     db_tables = getAllTables()
#     for i in db_tables:
#         for j in db_tables[i]:
#             # print("db read : ", i,j)
#             temp = getDataByTable(i,j)
#             content["/".join(["db",i,j])] = {
#                 "path" : "/".join(["db",i,j]),
#                 "data" : temp,
#                 "last_modified" : 0,
#                 "tokens" : tokenizer.tokenize_given_string(temp)
#             }

#     for i in content:
#         insert_file(content[i])

def downtime_checker():
    files = updateChecker(path)
    files_added = files['added']
    files_modified = files['modified']
    files_deleted = files['deleted']
    content = {}
    arr = []
    raw = {}

    for i in files:
        print("Files",i,len(files[i]))

    for i in files_deleted:
        delete_file(i)

    print("Reading Files ...")
    for i in files_modified:
        if i[:3] == 'db/':
            continue
        raw[i] = readFile(i)
        content[i] = remove_stopwords(raw[i] + " " + " ".join(i.split("\\")))
        arr.append(content[i])

    for i in files_added:
        if i[:3] == 'db/':
            continue
        raw[i] = readFile(i)
        content[i] = remove_stopwords(raw[i] + " " + " ".join(i.split("\\")))
        arr.append(content[i])

    for i in getAllData(): #from database
        arr.append(remove_stopwords(i))

    newRuleMiner(arr)
    tokenizer.text_tokenizer(arr)
    # print(tokenizer.word_index)

    for i in files_added:
        insert_file({
            "path" : i,
            "data" : content[i],
            "raw_data" : raw[i],
            "last_modified" : getLastModified(i),
            "tokens" : {}
        })

    db_tables = getAllTables()
    for i in db_tables:
        for j in db_tables[i]:
            # print("db read : ", i,j)
            temp = getDataByTable(i,j)
            insert_file({
                "path" : "/".join(["db",i,j]),
                "data" : temp + " ".join(["db",i,j]),
                "raw_data":"",
                "last_modified" : 0,
                "tokens" : {}
            })

    for i in files_modified:
        update_file({
            "path" : i,
            "data" : content[i],
            "raw_data" : raw[i],
            "last_modified" : getLastModified(i),
            "tokens" : {}
        })

def update_tokenizer():
    while True:
        if getAnyModified():
            print("Started updating the tokenizer ...")
            tokenizer.update()
            print("Updated tokenizer ....")
            setAnyModified()
        # time.sleep(1 * 60)
        time.sleep(10)

if __name__ == "__main__":

    init_db()

    newRuleMiner([i['data'] for i in select_all_files()])

    if not os.path.exists("sample.pickle"):
        newTokenizer("sample.pickle")
    downtime_checker()
    tokenizer.update()
    
    print("Server started at =", datetime.now().strftime("%H:%M:%S"))

    server_thread = myThread("Server", run_server, ("Server", 5678))
    server_thread.start()

    watch_dog_thread = myThread("WatchDog", run_watch_dog, ("WatchDog", path))
    watch_dog_thread.start()

    tokenizer_updater_thread = myThread("Tokenizer Updater", update_tokenizer, ())
    tokenizer_updater_thread.start()



