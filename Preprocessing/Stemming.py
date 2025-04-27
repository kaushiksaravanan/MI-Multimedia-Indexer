# coding=utf-8
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from collections import defaultdict
import codecs
import string
import snowballstemmer # type: ignore
import re
p = re.compile(u'[\u0900-\u097F]',flags=re.UNICODE)

def is_hindi(character):
    return bool(p.match(character))

porter_stemmer  = PorterStemmer()
tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

stemmer = snowballstemmer.stemmer('hindi');

def get_stem_english(text):
    tokens = word_tokenize(" ".join(text))
    lemma_function = WordNetLemmatizer()
    lemma=[]
    for token, tag in pos_tag(tokens):
        lemma.append(lemma_function.lemmatize(token, tag_map[tag[0]]))
    text = " ".join(lemma)
    tokenization = nltk.word_tokenize(text)
    wor=[]
    for w in tokenization:
        wor.append(porter_stemmer.stem(w))
    return wor


def get_stem_hindi(text):
    return stemmer.stemWords(text)

def stem_fun(text):
    eng=[]
    mix=[]
    hin=[]
    for wor in text.split():
        c=l=0
        for letter in wor:
            if(is_hindi(letter)):
               c+=1
            if letter!=',':
                l+=1
        if c==l:
            hin.append(wor)
        elif c==0:
            eng.append(wor)
        elif c!=0:
            mix.append(wor)
    # print(mix)

    return " ".join(get_stem_hindi(hin)+get_stem_english(eng)+mix)

if __name__ == "__main__":
    print(stem_fun("a quick brown fox jumps over a lazy dog जब आप कोई भाषा को सीखते हैं, तो उसमें आपको अक्षर, शब्द, वाक्य तथा वाक्यांश आदि को सीखना पड़ता है। एक सरल वाक्य वाक्य का प्रयोग किसी भाव या विचार को व्यक्त करने के लिए किया जाता है। यदि आप अंग्रेजी सीख रहे  (simple sentence) हैं तो आपको सरल वाक्यों का ज्ञान होना आवश्यक है।"))
