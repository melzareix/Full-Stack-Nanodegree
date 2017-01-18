from google.appengine.ext import db


class UserModel(db.Model):
    """
        Model for User.
    """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
