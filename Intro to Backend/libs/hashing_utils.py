from google.appengine.ext import vendor
import hashlib

vendor.add("libs")
from bcrypt import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_same_password(password, hashed):
    return bcrypt.hashpw(password, hashed) == hashed


def hash_cookie(user_id):
    hashed_id = hashlib.sha256(user_id).hexdigest()
    return "%s|%s" % (user_id, hashed_id)


def is_cookie_valid(cookie):
    c, h = cookie.split("|")
    return hash_cookie(c) == cookie
