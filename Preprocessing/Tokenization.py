import pickle
import os.path
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from collections import Counter
from Server.orm import select_all_files, update_file

class TokenClass:
  token_list = {}
  tokenizer1 = Tokenizer(num_words=10**9)

  def __init__(self,path="Pickledfile.pickle"):

    self.path = path

    print()
    print("CWD :", os.getcwd())
    print("Does {} exists : ".format(self.path), os.path.exists(self.path))

    if(os.path.exists(self.path)):
          dbfile = open(self.path, 'rb')     #loading(also reading) pickle
          db = pickle.load(dbfile)
          self.tokenizer1 = db
          self.tokenizer1.word_index = db.word_index
          print(path + " file found")
    else:
        self.tokenizer1 = Tokenizer(num_words=10**9)
        print("Initializing a new tokenizer")
        # self.update()

    d = self.tokenizer1.word_index
    self.token_list = {d[i]:i for i in d}
   
  def text_tokenizer(self,arr):  
    self.tokenizer1.fit_on_texts(arr)
    self.save()
    d = self.tokenizer1.word_index
    self.token_list = {d[i]:i for i in d}

  def tokenize_given_string(self,s):
     d = self.tokenizer1.texts_to_sequences([s])
     return dict(Counter(d[0]))

  def save(self):
     dbfile = open(self.path, 'wb')   # storing pickle
     pickle.dump(self.tokenizer1, dbfile)                     
     dbfile.close()
     print("tokenizer saved")

  def dot_product(self, arr1, arr2):
     x = dict(Counter(arr1))
     y = dict(Counter(arr2))
     result = list(set(x.keys()) & set(y.keys()))
     Dot = 0
     for i in result:
         Dot += x[i]*y[i]
     return(Dot)

  def dot_product_dict(self,x,y):
    result = list(set(x.keys()) & set(y.keys()))
    result.sort()
    Dot = 0
    for i in result:
        Dot += x[i]*y[i]
    return(Dot)

  def update(self, newObject = False):
    files = select_all_files()
    corpus = [i['data'] for i in files]
    if newObject:
      self.tokenizer1 = Tokenizer(num_words=10**15)
    self.tokenizer1.fit_on_texts(corpus)
    self.save()
    d = self.tokenizer1.word_index
    self.token_list = {d[i]:i for i in d}

    allFile = select_all_files()
    for i in allFile:
      temp = i
      temp['tokens'] = dict(Counter(self.tokenizer1.texts_to_sequences([temp['data']])[0]))
      update_file(temp)


def newTokenizer(path):
  tokenizer = TokenClass(path)

tokenizer = TokenClass("sample.pickle")

if __name__ == "__main__":
  p1 = TokenClass()
  p1.text_tokenizer(["I am Harishanakr", "मुक्त ज्ञानकोश विकिपीडिया से नेविगेशन पर जाएँखोज पर जाएँ इस पृष्ठ पर इन्टरनेट पर उपलब्ध विभिन्न हिन्दी एवं देवनागरी सम्बंधित साधनों की कड़ियों की सूची है इसमें ऑनलाइन एवं ऑफ़लाइन उपकरण (टूल्स) शामिल हैं"])
  p1.word_index
  p1.dot_product([1,1,4,5,4,6,5],[11,11,22,33,11,11,11,1,1,1,1,4,5])
