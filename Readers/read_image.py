# import easyocr

'''################
To use ocr first from other files add these lines 

from read_image import *              --module import
reader = easyocr.Reader(['hi','en'])  --hindi and english text recogintion 
read_text(reader,image_file_to_read)  --returns a list of text detected

###################''' 

import easyocr
reader = easyocr.Reader(['hi','en'])
def read_image(path):
    result = reader.readtext(path)
    text=[]
    for i in result:
        text.append(i[-2])
    return text
