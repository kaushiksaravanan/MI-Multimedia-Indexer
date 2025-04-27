import os
from flask import Flask, redirect, render_template, request, url_for, jsonify, Blueprint
from flask.wrappers import Response
from markupsafe import escape
import subprocess
from flask_restful import Resource, Api
from dataclasses import dataclass
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from json import dumps, loads
import warnings
import logging
import re
import string

from SQLReader.SQLReader import getDataByTableAsHtml, getAllDatabases, getAllTablesOfDatabase
from Preprocessing.RemoveStopWords import remove_stopwords
from Preprocessing.Tokenization import tokenizer
from Preprocessing.RuleMining import RuleMiner, newRuleMiner
from Server.orm import getAll, getFileRaw

app = Flask(__name__)
file_system = Blueprint('file_system', __name__, url_prefix='/files', static_folder='../../SmartIndiaHackathon2022')
app.register_blueprint(file_system)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../db01_demo.db"
# logging.basicConfig(level=logging.DEBUG)

# db = SQLAlchemy(app)
# api = Api(app)
PORT = 5678

@app.route("/")
def home():
    return render_template("home.html",)

@app.route("/search_prcss", methods=["POST"])
def search_request():
    if request.method == "POST":
        search_term = request.form["search_term"].strip().lower()
        return redirect(url_for('search', param=search_term))

@app.route("/open/db")
def all_databases():
    return getAllDatabases()

@app.route("/open/db/<dbname>")
def all_tables_of_database(dbname):
    params = dict(request.args)
    return getAllTablesOfDatabase(dbname)

@app.route("/open/db/<dbname>/<tablename>")
def db_display(dbname, tablename):
    conditions = dict(request.args)
    query = ""
    if 'query_search' in conditions:
        query = conditions.pop('query_search')

    values_dicts,columns = getDataByTableAsHtml(dbname, tablename, conditions, search_query = query)
    # return dumps(values_dicts)
    return render_template("record.html", columns=columns, dicts=values_dicts, query_search=query)

@app.route("/open_simple/db/<dbname>/<tablename>")
def db_display_simple(dbname, tablename):
    conditions = dict(request.args)
    # print(conditions)
    query = ""
    if 'query_search' in conditions:
        query = conditions.pop('query_search')

    values_dicts,columns = getDataByTableAsHtml(dbname, tablename, conditions, search_query = "")
    # return dumps(values_dicts)
    return render_template("record2.html", columns=columns, dicts=values_dicts, query_search="")

@app.route("/q/<param>")
def search(param):
    # print(escape(param))
    # print(param)
    arr = []
    tokens = tokenizer.tokenize_given_string(param)
    print(RuleMiner.conss_list)
    related = RuleMiner.mine(param)
    token_dict = {tokenizer.token_list.get(i,""):tokens.get(i,0) for i in tokens}
    # print(token_dict)
    token_list = list(token_dict.keys())

    allFile = getAll()
    
    for i in allFile:
        d = i.__dict__
        # print(d)
        d['tokens'] = intKeys(loads(d['tokens']))
        d['score'] = tokenizer.dot_product_dict(d['tokens'], tokens)

        d['pure_tokens'] = [
            tokenizer.token_list.get(i,"") for i in tokenizer.tokenize_given_string(d['data'])
        ]
        d['pure_tokens'] = [i for i in d['pure_tokens'] if i in token_list]
        if d['score'] > 0:
            arr.append(d)
    
    sorter = lambda x : x['score']
    arr = sorted(arr, key=sorter, reverse=True)
    
    return render_template("index2.html", context={"search_term": param, "content":arr}, tokens=token_list)

def intKeys(d):
    temp = {}
    for i in d:
        temp[int(i)] = d[i]
    return temp

@app.route("/open/<path>")
def open(path):
    params = dict(request.args)
    query = remove_stopwords(params["query_search"]).strip(string.punctuation)
    command = [path.replace("<->", "\\")]
    # print(command[0])
    try:
        subprocess.check_output(command[0], timeout=0.5, shell=True)
    except:
        pass
    return render_template("highlight.html", path=path.replace("<->", "\\"), content=getFileRaw(path), search_query=query)

def fileJSON(file):
    """Converts file object to JSON

    Args:
        file (File): Object of database model 'File'

    Returns:
        JSON: JSON version of the object 'file' for HTTP requests.
    """
    return {
            "path": str(file.path),
            "last_modified": float(file.last_modified),
            "data": str(file.data),
            "tokens" : loads(file.tokens)
        }

# @dataclass
# class File(db.Model):
#     path: str
#     last_modified: str
#     data: str
#     tokens: str
    
#     path = db.Column(db.String(1000), primary_key = True)
#     last_modified = db.Column(db.Numeric(10, 6), nullable = False)
#     data = db.Column(db.String(10**6), nullable=False)
#     tokens = db.Column(db.UnicodeText(), nullable=False)
    

# class FileListAPI(Resource):
#     def get(self):
#         # print(db.engine.table_names())
#         try:
#             # return jsonify(File.query.all())
#             lst = []
#             for i in File.query.all():
#                 lst += [fileJSON(i),]
#             # print(lst)
#             return lst
#         except:
#             # print(File.query.all())
#             return "Hello"
    
#     def post(self):
#         try:
#             new_file = File(path = request.json["path"], data=request.json["data"], last_modified = request.json["last_modified"], tokens=dumps(request.json["tokens"]))
#             db.session.add(new_file)
#             db.session.commit()
#             return fileJSON(new_file)
#         except Exception as e:
#             return Response(f"Exception@{e.args}: Please check the attributes", status=HTTPStatus.NOT_ACCEPTABLE)
        
#     def patch(self):
#         file = File.query.filter_by(path=request.json["path"]).first_or_404()
#         if "data" in request.json:
#             #* File content modification
#             file.data = request.json["data"]
#             file.last_modified = request.json["last_modified"]
            
#         if "path" in request.json:
#             #* Moving the file
#             file.path = request.json["path"]
            
#         if "tokens" in request.json:
#             file.tokens = dumps(request.json["tokens"])
        
#         db.session.commit()
        
#         file = File.query.filter_by(path=request.json["path"]).first()
#         return fileJSON(file)

# class FileAPI(Resource):
#     def get(self, path):
#         print(db.engine.table_names())
#         file = File.query.filter_by(path=path).first_or_404()
#         return fileJSON(file)
    
#     def patch(self, path):
#         file = File.query.filter_by(path=path).first_or_404()
        
#         if "data" in request.json:
#             #* File content modification
#             file.data = request.json["data"]
#             file.last_modified = request.json["last_modified"]
            
#         if "path" in request.json:
#             #* Moving the file
#             file.path = request.json["path"]
        
#         if "tokens" in request.json:
#             file.tokens = dumps(request.json["tokens"])
        
#         db.session.commit()
        
#         file = File.query.filter_by(path=path).first()
#         return fileJSON(file)
    
#     def delete(self, path):
#         file = File.query.filter_by(path=path).first_or_404(path)
#         db.session.delete(file)
#         db.session.commit()
#         return fileJSON(file)
    

# #! Endpoints
# api.add_resource(FileListAPI, "/files")
# api.add_resource(FileAPI, "/files/<path>")
    
if __name__ == "__main__":
    # db.create_all()
    # print(db.engine.table_names())
    app.run(port=PORT)