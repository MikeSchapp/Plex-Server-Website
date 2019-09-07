import bcrypt

from secret_store.config import plex_login, plex_password, flask_secret_key


def hash_pass(**kwargs):
    password = kwargs["password"]
    b_password = bytes(password, 'ascii')
    hashed_pass = bcrypt.hashpw(b_password, bcrypt.gensalt())
    return hashed_pass


def check_plex_un_pw(**kwargs):
    try:
        username = kwargs["username"]
        password = kwargs["password"]
        encoded_password = bytes(password, 'ascii')
        encoded_username = bytes(username, 'ascii')
        if bcrypt.checkpw(encoded_password, plex_password) and bcrypt.checkpw(encoded_username, plex_login):
            return True
        else:
            return False
    except TypeError:
        return False


def check_pw(**kwargs):
    try:
        password = kwargs["password"]
        encoded_password = bytes(password, 'ascii')
        if bcrypt.checkpw(encoded_password, flask_secret_key):
            return True
        else:
            return False
    except TypeError:
        return False
