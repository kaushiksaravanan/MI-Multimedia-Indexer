from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, String, Numeric, UnicodeText, DECIMAL, create_engine, select
from sqlalchemy.exc import NoResultFound
from json import dumps, loads
import os
import datetime
import warnings


db = declarative_base()
# engine = create_engine("sqlite:///db01_demo.db", future=True, connect_args={'check_same_thread': False})
# engine = create_engine(f"mysql+pymysql://root:{password}@127.0.0.1:3306/SIH", future=True)
engine = create_engine(f"postgresql+psycopg2://postgres:{'root'}@127.0.0.1:5432/Tokens", future=True)
session = Session(engine)


class File(db):
    __tablename__ = "file"

    path = Column(String(1000), primary_key=True)
    last_modified = Column(Numeric(10, 6, asdecimal=False), nullable=False)
    raw_data = Column(UnicodeText(), nullable=False)
    data = Column(UnicodeText(), nullable=False)
    tokens = Column(UnicodeText(), nullable=False)

    # Official string representation of a file object.
    def __repr__(self) -> str:
        return f"File(path={self.path!r}, last_modified={self.last_modified}, data={self.data!r}, tokens={self.tokens!r}"


def lastmodified(file_path=None):
    if file_path is None:
        stmt = select(File)
        master_dict = {}
        for file in session.scalars(stmt):

            master_dict[file.path] = datetime.datetime.utcfromtimestamp(
                file.last_modified).strftime('%Y-%m-%d %H:%M:%S')

        return master_dict

    try:
        stmt = select(File).where(File.path == file_path)
        file = session.scalars(stmt).one()

        # return datetime.datetime.utcfromtimestamp(file.last_modified).strftime('%Y-%m-%d %H:%M:%S')
        return file.last_modified
    except NoResultFound as e:
        return f"Not found {type(e)}"


def tokens(file_path=None):
    session = Session(engine)
    if file_path is None:
        stmt = select(File)
        # print(stmt)
        master_dict = {}
        for file in session.scalars(stmt):
            req_dict = {file.path: loads(file.tokens)}
            master_dict.update(req_dict)

        return master_dict

    try:
        stmt = select(File).where(File.path == file_path)
        file = session.scalars(stmt).one()
        return {
            file_path: loads(file.tokens)
        }
    except NoResultFound as e:
        return f"Not found {type(e)}"


def init_db():
    db.metadata.create_all(engine)


def delete_file(file_path):
    with Session(engine) as session:
        try:
            stmt = select(File).where(File.path == file_path)
            file = session.scalars(stmt).one()
            # print(file, type(file))
            session.delete(file)
            session.commit()
        except NoResultFound as e:
            return f"Not found {type(e)}"

def insert_file(file_dict, server_update=False):
    """Inserting a file into the database
    Args:
        file_dict (dict): Keys of the dictionary: path, last_modified, data, tokens
    """

    with Session(engine) as session:
        # The below line of code essentially serializes the JSON (python dictionary here) to a unicode text.
        file_dict["tokens"] = dumps(file_dict["tokens"])
        new_file = File(**file_dict)
        if server_update:
            # print(new_file)
            pass
        try:
            session.add(new_file)
            session.commit()
            session.flush()
            return "\nSuccessful"
        except Exception as e:
            print(e)
            return "\nUnsuccessful"


def getAll():
    return session.query(File).all()

# def update_file(file_dict, server_update=False):
#     """Updating a file into the database
#     Args:
#         file_dict (dict): Keys of the dictionary: path, last_modified, data, tokens
#     """
#     delete_file(file_dict['path'])
#     insert_file(file_dict,server_update=server_update)

def update_file(file_dict):
    """Updating a file into the database
    Args:
        file_dict (dict): Keys of the dictionary: path, last_modified, data, tokens
    """
    with Session(engine) as session:
        try:
            file_dict["tokens"] = dumps(file_dict["tokens"])
            # print(file_dict)
            session.query(File).\
                filter(File.path == file_dict["path"]).\
                update(file_dict)
            session.commit()
        except NoResultFound as e:
            return f"Not found {type(e)}"

def getFileRaw(path):
    path = path.replace("<->", "\\")
    # print("Path of file :", path)
    with Session(engine) as session:
        try:
            res = (session.query(File).filter_by(path = path).all())
            # print(res)
            res = res[0]
            res = res.__dict__
            if "raw_data" in res:
                temp = res['raw_data']
                if temp is None:
                    return res['data']
                else:
                    return temp
            else:
                return res['data']
        except NoResultFound as e:
            return f"Not found {type(e)}"

def select_all_files():
    file_list = []
    for i in session.query(File).all():
        file_list.append({
            "path": i.path,
            "last_modified": i.last_modified,
            "data": i.data,
            "tokens": loads(i.tokens)
        })

    return file_list


if __name__ == "__main__":
    pass
    # init_db()
    # print("OUTPUT: ")
    # print(lastmodified())
    # print(lastmodified("requirements3.txt"))
    # print("--------------")
    # print(tokens())
    # print(tokens("requirements3.txt"))

    # # print(select_all_files())

    # session.scalars are used for returning the retrieved results as scalars
