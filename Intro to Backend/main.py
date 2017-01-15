#!/usr/bin/env python
import webapp2
import jinja2
import os
import re
import cgi
from google.appengine.ext import db
from google.appengine.ext import vendor

vendor.add("libs")
import hashing_utils

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handle(webapp2.RequestHandler):
    """
        Base class for handlers, includes several helpful methods.
    """

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get_logged_in_user(self):
        username_cookie = self.request.cookies.get('username')
        user = None
        if Validate.is_user_logged_in(username_cookie):
            user = UserModel.get_by_id(long(username_cookie.split("|")[0]))
        return user


# Database Models
class UserModel(db.Model):
    """
        Model for User.
    """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False)


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


class PostLike(db.Model):
    """
        Model for a Like on a post.
    """
    post = db.ReferenceProperty(PostModel, collection_name='post_likes')
    user = db.ReferenceProperty(UserModel, collection_name='posts_I_liked')


class PostComment(db.Model):
    """
        Model for a Comment on a Post.
    """
    post = db.ReferenceProperty(PostModel, collection_name='post_comments')
    user = db.ReferenceProperty(UserModel, collection_name='comments_I_made')
    content = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)


# Main Handler
class MainHandler(Handle):
    '''
        Handler for the Index page.
    '''

    def get(self):
        posts = db.GqlQuery("SELECT * FROM PostModel ORDER BY timestamp DESC")
        self.render('index.html', posts=posts, user=self.get_logged_in_user())


# User Reg/Login Handlers

class Validate(object):
    """
        Helper class for Validation.
    """
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

    @staticmethod
    def valid_username(username):
        return Validate.USER_RE.match(username)

    @staticmethod
    def valid_password(password):
        return Validate.PASS_RE.match(password)

    @staticmethod
    def valid_email(email):
        return Validate.EMAIL_RE.match(email)

    @staticmethod
    def is_user_logged_in(username_cookie):
        return username_cookie is not None and hashing_utils.is_cookie_valid(username_cookie)


class SignUp(Handle):
    """
        Handler for User Signup.
    """

    def get(self):
        username_cookie = self.request.cookies.get('username')
        if Validate.is_user_logged_in(username_cookie):
            self.redirect("/myprofile")
        else:
            self.render("signup.html", user=self.get_logged_in_user())

    def post(self):
        errors = []
        username = self.request.get("username")
        password = self.request.get("password")
        verifypassword = self.request.get("verify")
        email = self.request.get("email")

        if not username or not Validate.valid_username(username):
            errors.append("Please enter a valid username.")

        if not password or not Validate.valid_password(password):
            errors.append("Please enter a valid Password.")

        if not verifypassword or not password or (password != verifypassword):
            errors.append("The entered passwords don't match.")

        if email and (not Validate.valid_email(email)):
            errors.append("Please enter a valid email.")

        # Try to add user to database
        if len(errors) == 0:
            query = "WHERE username = '%s'" % username
            users_with_username = UserModel.gql(query).get()
            if users_with_username is not None:
                errors.append("Username Already Exists")
            else:
                user = UserModel(username=username, password=hashing_utils.hash_password(password), email=email)
                user.put()
                self.set_cookies(user)
                self.redirect("/myprofile")

        self.render("signup.html", errors=errors, user=self.get_logged_in_user())

    def set_cookies(self, user):
        user_id = str(user.key().id())
        self.response.set_cookie('username', hashing_utils.hash_cookie(user_id), max_age=2592000, path='/')


class Login(Handle):
    """
        Handler for User login.
    """

    def get(self):
        username_cookie = self.request.cookies.get('username')
        if Validate.is_user_logged_in(username_cookie):
            self.redirect("/myprofile")
        else:
            self.render("login.html", user=self.get_logged_in_user())

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        query = "WHERE username = '%s'" % username
        user = UserModel.gql(query).get()
        if user and hashing_utils.is_same_password(password, user.password):
            self.redirect("/myprofile")
            self.set_cookies(user)
        else:
            self.render("login.html", errors=["Wrong Username/Password combination."], user=self.get_logged_in_user())

    def set_cookies(self, user):
        user_id = str(user.key().id())
        self.response.set_cookie('username', hashing_utils.hash_cookie(user_id), max_age=2592000, path='/')


class LogoutHandler(Handle):
    """
        Handler for User logout.
    """

    def get(self):
        self.response.delete_cookie('username')
        self.redirect("/signup")


# User Profile Handler

class ProfileHandler(Handle):
    """
        Handler for /myprofile Page.
    """

    def get(self):
        username = self.request.cookies.get('username')
        if Validate.is_user_logged_in(username):
            user = UserModel.get_by_id(long(username.split("|")[0]))
            self.render("myprofile.html", user=user)
        else:
            self.redirect("/login")


# Post(s) Handlers
class NewPostHandler(Handle):
    """
        Handler for creating a new Post.
    """

    def get(self):
        if Validate.is_user_logged_in(self.request.cookies.get('username')):
            self.render('newpost.html', user=self.get_logged_in_user())
        else:
            self.redirect("/login")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if not Validate.is_user_logged_in(self.request.cookies.get('username')):
            self.redirect("/login")
        else:
            errors = []
            if not subject:
                errors.append("Post must have a title.")
            if not content:
                errors.append("Post must have a desc.")
            if subject and content:
                post = PostModel(subject=subject, content=content, post_creator=self.get_logged_in_user())
                post.put()
                self.redirect("/" + str(post.key().id()))
            else:
                self.render("newpost.html", subject=subject, content=content, errors=errors,
                            user=self.get_logged_in_user())


class EditPostHandler(Handle):
    """
        Handler for editing posts.
    """

    def get(self, post_id):
        post = PostModel.get_by_id(long(post_id))
        if post:
            post_creator_id = post.post_creator.key().id()
            if self.get_logged_in_user().key().id() == post_creator_id:
                self.render("editpost.html", post=post, user=self.get_logged_in_user())
            else:
                self.redirect("/")
        else:
            self.redirect("/")

    def post(self, post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        post = PostModel.get_by_id(long(post_id))

        if not post:
            self.redirect("/")
        else:
            errors = []
            if not subject:
                errors.append("Post must have a title.")
            else:
                post.subject = subject

            if not content:
                errors.append("Post must have a desc.")
            else:
                post.content = content

            if subject and content:
                post.put()
                self.redirect("/" + str(post.key().id()))
            else:
                self.render("editpost.html", post=post, errors=errors, user=self.get_logged_in_user())


class DeletePostHandler(Handle):
    """
        Handler for deleting posts.
    """

    def get(self, post_id):
        post = PostModel.get_by_id(long(post_id))
        if post:
            post_creator_id = post.post_creator.key().id()
            if self.get_logged_in_user().key().id() == post_creator_id:
                for post_comment in post.post_comments:
                    post_comment.delete()
                post.delete()
            self.redirect("/")
        else:
            self.redirect("/%s" % post_id)


class LikePostHandler(Handle):
    """
        Handler for post like.
    """

    def get(self, post_id):
        post = PostModel.get_by_id(long(post_id))
        if not post or (post.post_creator.key().id() == self.get_logged_in_user().key().id()):
            self.redirect("/")
        else:
            like_error = True
            if self.get_logged_in_user().key().id() not in [x.user.key().id() for x in post.post_likes]:
                like = PostLike(user=self.get_logged_in_user(), post=post)
                like.put()
                like_error = False
            self.render("blogpost.html", post=post, user=self.get_logged_in_user(), like_error=like_error)


class ViewPostHandler(Handle):
    """
        Handler for viewing a specific post.
    """

    def get(self, post_id):
        post = PostModel.get_by_id(long(post_id))
        if not post:
            self.redirect("/")
        else:
            self.render("blogpost.html", post=post, user=self.get_logged_in_user())


# Handlers for Comments Section

class NewCommentHandler(Handle):
    """
        Handler for adding a new comment.
    """

    def get(self, post_id):
        post = PostModel.get_by_id(long(post_id))
        if not post or not self.get_logged_in_user():
            self.redirect("/")
        else:
            self.render("newcomment.html", user=self.get_logged_in_user())

    def post(self, post_id):
        post = PostModel.get_by_id(long(post_id))
        if not post:
            self.redirect("/")
        else:
            comment_desc = self.request.get("comment")
            errors = []
            if not comment_desc:
                errors.append("Comment must not be empty.")

            if len(errors) == 0:
                comment = PostComment(post=post, user=self.get_logged_in_user(), content=comment_desc)
                comment.put()
                self.redirect("/%s" % post_id)
            else:
                self.render("newcomment.html", content=comment_desc, user=self.get_logged_in_user(), errors=errors)


class EditCommentHandler(Handle):
    """
        Handler for comment editing.
    """

    def get(self, post_id, comment_id):
        post = PostModel.get_by_id(long(post_id))
        comment = PostComment.get_by_id(long(comment_id))

        if not post or not comment:
            self.redirect("/")
        elif comment.key().id() not in [x.key().id() for x in post.post_comments]:
            self.redirect("/")
        elif self.get_logged_in_user().key().id() != comment.user.key().id():
            self.redirect("/")
        else:
            self.render('newcomment.html', content=comment.content, user=self.get_logged_in_user())

    def post(self, post_id, comment_id):
        post = PostModel.get_by_id(long(post_id))
        comment = PostComment.get_by_id(long(comment_id))

        if not post or not comment:
            self.redirect("/")
        elif comment.key().id() not in [x.key().id() for x in post.post_comments]:
            self.redirect("/")
        elif self.get_logged_in_user().key().id() != comment.user.key().id():
            self.redirect("/")
        else:
            comment_desc = self.request.get("comment")
            errors = []
            if not comment_desc:
                errors.append("Comment must not be empty.")

            if len(errors) == 0:
                comment.content = comment_desc
                comment.put()

            self.redirect("/%s" % post_id)


class DeleteCommentHandler(Handle):
    """
        Handler for Comment deletion.
    """

    def get(self, post_id, comment_id):
        post = PostModel.get_by_id(long(post_id))
        comment = PostComment.get_by_id(long(comment_id))

        if (not post) or (not comment):
            self.redirect("/")
        elif comment.key().id() not in [x.key().id() for x in post.post_comments]:
            self.redirect("/")
        elif self.get_logged_in_user().key().id() != comment.user.key().id():
            self.redirect("/")
        else:
            comment.delete()
        self.redirect("/%s" % post_id)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPostHandler),
    ('/signup', SignUp),
    ('/login', Login),
    ('/logout', LogoutHandler),
    ('/myprofile', ProfileHandler),
    ('/(\d+)/edit', EditPostHandler),
    ('/(\d+)/del', DeletePostHandler),
    ('/(\d+)/like', LikePostHandler),
    ('/(\d+)/comment/edit/(\d+)', EditCommentHandler),
    ('/(\d+)/comment/del/(\d+)', DeleteCommentHandler),
    ('/(\d+)/comment', NewCommentHandler),
    ('/(\d+)', ViewPostHandler)], debug=True)
