import os, re, json, textract, io
from PIL import Image
import openpyxl
import pandas as pd

def lastModified(path):
    return os.path.getmtime(path)

def readSpreadSheet(src):
    wb = openpyxl.load_workbook(src)
    arr = []
    for sheet in wb.sheetnames:
        arr.append(sheet)
        df = pd.read_excel (src, sheet_name=sheet)
        s = " ".join(list(df.columns))
        arr.append(s)
    return "\n".join(arr)

def readHumanReadableText(src):
    with io.open(src,'r',encoding='utf8') as f:
        text = f.read()
        return text

if __name__ == "__main__":
    # print(readSpreadSheet("SampleFiles/hindi.xlsx"))
    # print(readHumanReadableText("SampleFiles/README.md"))
    # print(readImage("D:\\SIH-new\\static\\images.png"))
    print(readSpreadSheet('SampleFiles\\hindi.xlsx'))
