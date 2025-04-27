import re
import nltk
from nltk.corpus import stopwords
from Preprocessing.Stemming import stem_fun
hindi_stopwords = ['हैं','है','|']

with open('Preprocessing/stopwords.txt', encoding='utf-8') as f:
  tmp=f.read().split('\n')
  for i in tmp:
    hindi_stopwords.append(i.strip())

def remove_english_stopwords(txt):
  stop = list(set(stopwords.words("english")))
  pattern = re.compile('\b(' + r'|'.join(stop) + r')\b')
  text = pattern.sub(r'', txt)
  text=re.sub('\s+',' ',text).strip()
  return text

def remove_hindi_stopwords(txt):
  # pattern = re.compile(r'\b(' + r'|'.join(hindi_stopwords) + r')\b')
  # text = pattern.sub('', txt)
  # text=re.sub('\s+',' ',text)
  text=''
  for i in txt.split(' '):
     if i not in hindi_stopwords:
        text += i+' '
  return text.strip()

def remove_stopwords(s):
  # s = ''.join(i for i in s if not i.isdigit())
  commas = re.compile(',+')
  s = commas.sub(' ', s)
  # s = s.replace("!@#$%^&*()[]{};:,./<>?\|`~-=_+1234567890", " ")
  t = remove_english_stopwords(s)
  # return remove_hindi_stopwords(stem_fun(t))
  return remove_hindi_stopwords(t)
