from docx2python import docx2python
from docx2python.iterators import iter_paragraphs
from Readers.read_image import *
import os
import glob
import shutil


#  Try to cache this line this needs to be run only once takes upto 2gb of space while running
reader = easyocr.Reader(['hi','en'])


# import codecs
# file = codecs.open("lol", "w", "utf-8")  template to test the write of text

def read_doc(path):
    '''
    Returns the text present in a docx file.

            Parameters:
                    path (string): A string for the document
            Returns:
                    text+img_txt(str): List consisting of all text in document
    '''
    location=path
    file_name='temp_images'
    imag_dir=file_name+'/images'

    doc=docx2python(location)
    text=[]
    text_all =[iter_paragraphs(doc.header),iter_paragraphs(doc.footer),iter_paragraphs(doc.body),iter_paragraphs(doc.footnotes),iter_paragraphs(doc.endnotes)]
    for i in text_all:
        for content in i:
            y=content.split()
            if len(y)!=0:
                    for ii in y:
                        text+=y
    docx2python(location,imag_dir)
    img_txt=[]
    directory = imag_dir
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            img_txt += read_image(f)
    shutil.rmtree(directory)
    return " ".join(text+img_txt)

# print(read_doc('w1.docx'))
