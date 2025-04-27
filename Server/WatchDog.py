import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, requests
from Server.Server import PORT
from Server.orm import delete_file, insert_file, update_file
from Server.UpdationChecker import getLastModified
from Preprocessing.RemoveStopWords import remove_stopwords
from Preprocessing.Tokenization import tokenizer, newTokenizer
from Readers.Reader import readFile
import datetime
import json

anyModified = False

def getAnyModified():
    return anyModified

def setAnyModified(status = False):
    global anyModified
    anyModified = status

class OnMyWatch:
    def __init__(self, path = os.getcwd()):
        self.observer = Observer()
        self.watchDirectory = path

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        global anyModified
        url = "http://127.0.0.1:{}/{}"
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            if event.src_path.endswith(".crdownload"):
                return
            print("Created : {}".format(event.src_path), datetime.datetime.now())
            raw_data = readFile(event.src_path)
            content = remove_stopwords(raw_data + " " + " ".join(event.src_path.split("\\")))
            tokenizer.tokenizer1.fit_on_texts([content])
            data = {
                "path" : event.src_path,
                "data" : content,
                "raw_data" : raw_data,
                "last_modified" : getLastModified(event.src_path),
                "tokens" : tokenizer.tokenize_given_string(content)
            }
            insert_file(data)
            setAnyModified(True)

        elif event.event_type == 'modified':
            if event.src_path.endswith(".crdownload"):
                return
            print("Modified : {}".format(event.src_path), datetime.datetime.now())
            setAnyModified(True)
            raw_data = readFile(event.src_path)
            content = remove_stopwords(raw_data + " " + " ".join(event.src_path.split("\\")))

            try:
                data = {
                    "path" : event.src_path,
                    "data" : content,
                    "raw_data" : raw_data,
                    "last_modified" : getLastModified(event.src_path),
                    "tokens" : tokenizer.tokenize_given_string(content)
                }
                update_file(data)
            except FileNotFoundError as e:
                    print(str(e))
                    print("File note copied/moved/downloaded properly ...")

        elif event.event_type == 'deleted':
            if event.src_path.endswith(".crdownload"):
                return
            print("Deleted : {}".format(event.src_path), datetime.datetime.now())
            delete_file(event.src_path)
            setAnyModified(True)
            
        else:
            print("Unspecified Operation")
            print(event.event_type, event.src_path)

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
