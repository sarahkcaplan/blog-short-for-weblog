from base import BaseHandler
from models.user import User
from models.post import Post
from models.comments import Comments
from google.appengine.ext import db

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

# Page for creating new posts.
# Successful post redirects to post's permalink location.
class NewPost(BaseHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")

        else:
            self.redirect('/signup')

    def post(self):
        if self.user:
            subject = self.request.get("subject")
            content = self.request.get("content")
            uid = int(self.read_secure_cookie('user_id'))
            user = User.by_id(uid)
            author = str(user.name)

            if subject and content:
                # This is invoking a model class constructor
                p = Post(parent=blog_key(), subject=subject, content=content,
                         author=author, liked_by=[])
                p.put()

                self.redirect("/blog/%s" % str(p.key().id()))

            else:
                error = "We need both a title and some text"
                self.render("newpost.html", subject=subject,
                            content=content, error=error)

        else:
            self.redirect('/signup')

# Handler for post's permalink pages. Gets post_id from URI.
class PostPage(BaseHandler):
    def get(self, post_id, comment_id=None):
        if self.user:
            post = Post.post_query(post_id)
            uid = int(self.read_secure_cookie('user_id'))
            user = User.by_id(uid)
            current_user = str(user.name)

            if uid in post.liked_by:
                liking_user = uid

            else:
                liking_user = None

            comment = Comments.all().order("-last_modified")
            comments = comment.filter("post_id =", post_id)

            likes_count = len(post.liked_by)

            self.render("post.html", liking_user=liking_user,
                    current_user=current_user, post=post,
                    likes_count=likes_count,
                    comments=comments, post_id=post_id)

        else:
            self.redirect('/signup')


# Handler for deleting post
class DeletePost(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id):
        post = Post.post_query(post_id)

        if self.user and self.user == post.author:
            post.delete()
            self.redirect('/blog/')

        else:
            self.redirect('/signup')



# Handler for editing post
class EditPost(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id):
        post = Post.post_query(post_id)

        if self.user and self.user == post.author:
            self.render("editpost.html", post=post, post_id=post_id)

        else:
            self.redirect('/signup')

        if not post:
            self.error(404)
            return

    def post(self, post_id):
        post = Post.post_query(post_id)

        if self.user and self.user == post.author:
            subject = self.request.get("subject")
            content = self.request.get("content")

            if subject and content:
                post.subject = subject
                post.content = content
                post.put()
                self.redirect("/blog/%s" % str(post.key().id()))

            else:
                error = "We need both a title and some text"
                self.render("newpost.html", subject=subject, content=content,
                            error=error)
        else:
            self.redirect('/signup')
