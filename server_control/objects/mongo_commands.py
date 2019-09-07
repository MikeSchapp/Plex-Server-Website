from pymongo import MongoClient
import bcrypt
from secret_store.config import *


class MongoApi:

    def __init__(self, name):
        self.name = name
        self.client = MongoClient('localhost', 27017)
        self.create = self.client['users']
        self.db = self.create.users

    def hash_pass(self, **kwargs):
        password = kwargs["password"]
        b_password = bytes(password, 'ascii')
        hashed_pass = bcrypt.hashpw(b_password, bcrypt.gensalt())
        return hashed_pass

    def check_un_pw(self, **kwargs):
        try:
            username = kwargs["username"]
            password = kwargs["password"]
            encoded_password = bytes(password, 'ascii')
            hashed_account = self.db.find_one({'un': username}, {'pw': 1})
            hashed_password = hashed_account["pw"]
            if bcrypt.checkpw(encoded_password, hashed_password):
                return True
            return False
        except TypeError:
            return False

    def store_un_pw(self, **kwargs):
        password = self.hash_pass(**kwargs)
        username = kwargs["username"]
        self.db.insert_one({
            "un": username,
            "pw": password
        })

    def find_un_pw(self, username):
        return self.db.find_one({'un': username}, {'pw': 1})


