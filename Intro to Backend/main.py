#!/usr/bin/env python
import webapp2, jinja2, os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handle(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class PostModel(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)

    def __init__(self,
                 parent=None,
                 key_name=None,
                 _app=None,
                 _from_entity=False,
                 **kwds):
        super(PostModel, self).__init__(parent=None, key_name=None, _app=None, _from_entity=False, **kwds)
        self._render_text = self.content.replace('\n', '<br>')

class MainHandler(Handle):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM PostModel ORDER BY timestamp DESC")
        self.render('index.html', posts=posts)


class NewPost(Handle):
    def get(self):
        self.render('newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        errors = []
        success = False
        if not subject:
            errors.append("Post must have a title.")
        if not content:
            errors.append("Post must have a desc.")
        if subject and content:
            post = PostModel(subject=subject, content=content)
            post.put()
            self.redirect("/" + str(post.key().id()))
        self.render("newpost.html", subject=subject, content=content, errors=errors)


class ViewPost(Handle):
    def get(self, post_id):
        post = PostModel.get_by_id(long(post_id))
        if not post:
            self.redirect("/")
        else:
            self.render("blogpost.html", post=post)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPost),
    ('/(\d+)', ViewPost)], debug=True)
