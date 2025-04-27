import re
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
import json
import warnings
from collections import Counter
from sqlalchemy import inspect
from json import dumps
warnings.filterwarnings("ignore", category=DeprecationWarning)
import string
import random
from Preprocessing.RemoveStopWords import remove_stopwords

credits = [
    # {
    #     "server":"MySQL",
    #     "host":"localhost",
    #     "user":"root",
    #     "password":"root",
    #     "database":"demo1"
    # },
    {
        "server":"PostgreSQL",
        "host":"localhost",
        "user":"postgres",
        "password":"root",
        "database":"crime",
        "port":"5432"
    },
    {
        "server":"PostgreSQL",
        "host":"localhost",
        "user":"postgres",
        "password":"root",
        "database":"postgres",
        "port":"5432"
    }
    # {
    #     "server":"PostgreSQL",
    #     "host":"localhost",
    #     "user":"root",
    #     "password":"root",
    #     "database":"postgres",
    #     "port":"5432"
    # }
    # {
    #     "server":"sqlite3",
    #     "path":"D:\\employees_db-full-1.0.6.db",
    #     "database":"employees_db-full-1.0.6"
    # },
    # {
    #     "server":"sqlite3",
    #     "path":"D:\\database.sqlite",
    #     "database":"database_sqlite"
    # }
]

engines = {}

for i in credits:
    if i['server'] == 'sqlite3':
       engines[i['database']] = create_engine('sqlite:///{}'.format(i['path']), echo = False)
       engines[i['database']].connect()

    elif i['server'] == 'PostgreSQL':
        engines[i['database']] = create_engine("postgresql://{}:{}@{}/{}".format(i['user'], i['password'],i['host'],i['database']),echo = False)
        engines[i['database']].connect()

    elif i['server'] == 'MySQL':
        engines[i['database']] = create_engine("mysql://{}:{}@{}/{}".format(i['user'], i['password'],i['host'],i['database']),echo = False)
        engines[i['database']].connect()

def dfToStr(df):
    df.drop(['photo'], axis=1, inplace=True, errors='ignore')
    m = df.values.tolist()
    s = ""
    for i in m:
        # print(type(i))
        s += ", ".join([str(k) for k in i]) + "\n"
    return s[:-1]

def getAllDatabases():
    d = {}
    for i in credits:
        d[i["database"]] = {
            "name" : i["database"],
            "link" : "/open/db/" + i["database"],
            "server" : i["server"]
        }
    return dumps(d)

def getAllTablesOfDatabase(dbname):
    tables = engines[dbname].table_names()
    d = {}
    for i in tables:
        d[i] = {
            "name" : i,
            "link" : "/open/db/" + dbname + "/" + i
        }
    return dumps(d)

def getAllData():
    all_strings = []

    for i in engines:
        for j in engines[i].table_names():
            df = pd.DataFrame(pd.read_sql_table(str(j), engines[i]))
            df.drop(['photo'], axis=1, inplace=True, errors='ignore')
            df = df.fillna(' ')
            all_strings.append(dfToStr(df))
        
    return all_strings

def getDataByDatabase(dbname):
    all_strings = []

    for j in engines[dbname].table_names():
        df = pd.DataFrame(pd.read_sql_table(str(j), engines[dbname]))
        df.drop(['photo'], axis=1, inplace=True, errors='ignore')
        df = df.fillna(' ')
        all_strings.append(dfToStr(df))
        
    return all_strings

def getDataByTable(dbname, table):
    df = pd.DataFrame(pd.read_sql_table(table, engines[dbname]))
    df.drop(['photo'], axis=1, inplace=True, errors='ignore')
    df = df.fillna(' ')
    return dfToStr(df)

# def getDataByTableAsHtml(dbname, table, conditions={}):
#     df = pd.DataFrame(pd.read_sql_table(table, engines[dbname]))
#     df.drop(['photo'], axis=1, inplace=True, errors='ignore')
#     if bool(conditions):
#         for key in conditions:
#             df = df[df[key] == conditions[key]]
#     return df.to_html(classes='table table-stripped')

generate_string = lambda k : ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=k))

def getDataByTableAsHtml(dbname, table, conditions={}, is_open_simple = False, search_query = ""):
    df = pd.DataFrame(pd.read_sql_table(table, engines[dbname]))
    df.drop(['photo'], axis=1, inplace=True, errors='ignore')
    df = df.astype(str)
    if bool(conditions):
        for key in conditions:
            df = df[df[key] == conditions[key]]
    arr = list(df.T.to_dict().values())
    res = []
    references = getAllForeignKeys(dbname, table)
    new_query = remove_stopwords(search_query)
    regex = "(" + new_query.replace(" ", "|") + ")"
    # print(regex)

    for i in arr:
        temp = i
        keys = list(i.keys())
        string = " ".join(list(i.values()))
        # print(string, bool(re.findall(regex, string)))

        if (not re.findall(regex, string.lower())) and search_query != "":
            continue

        for key in keys:
            id = generate_string(20)
            if key in references:
                temp[key] = {
                    "value" : str(temp[key]),
                    "link" : "/open_simple/db/" + references[key] + temp[key],
                    "id" : id
                }
            else:
                temp[key] = {
                    "value" : str(temp[key]),
                    "id" : id
                }            

        res.append(temp)

    # print(res)
    if len(res) == 0:
        columns = []
    else:
        columns = [i for i in res[0].keys()]

    return res,columns

def getAllTables():
    d = {}
    for i in engines:
        d[i] = engines[i].table_names()
    return d
 
def getAllForeignKeys(dbname, table):
    inspector = inspect(engines[dbname])
    d = {}
    for i in inspector.get_foreign_keys(table_name=table):
        # print(table, i["constrained_columns"], i["referred_table"], i["referred_columns"])
        if len(i["constrained_columns"]) == 1 and len(i["referred_columns"]) == 1:
            d[i["constrained_columns"][0]] = dbname + "/" + i["referred_table"] + "?" + i["referred_columns"][0] + "="
    return d


if __name__ == "__main__":
    # print(getAllTables())

    inspector = inspect(engines['postgres'])

    for table in inspector.get_table_names():
        # print(table)
        for i in inspector.get_foreign_keys(table_name=table):
            # print(json.dumps(i, indent=4))
            print(table, i["constrained_columns"], i["referred_table"], i["referred_columns"])
        print()