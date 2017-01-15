from google.appengine.ext import db
from PostModel import PostModel
from UserModel import UserModel


class PostLike(db.Model):
    """
        Model for a Like on a post.
    """
    post = db.ReferenceProperty(PostModel, collection_name='post_likes')
    user = db.ReferenceProperty(UserModel, collection_name='posts_I_liked')
