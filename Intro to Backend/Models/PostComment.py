from google.appengine.ext import db
from PostModel import PostModel
from UserModel import UserModel


class PostComment(db.Model):
    """
        Model for a Comment on a Post.
    """
    post = db.ReferenceProperty(PostModel, collection_name='post_comments')
    user = db.ReferenceProperty(UserModel, collection_name='comments_I_made')
    content = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
