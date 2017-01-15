from google.appengine.ext import db
from UserModel import UserModel
import cgi


class PostModel(db.Model):
    """
        Model for Post.
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    post_creator = db.ReferenceProperty(UserModel, collection_name='posts')

    def render(self):
        self.content = cgi.escape(self.content, quote=True)
        return self.content.replace('\n', '<br>')
