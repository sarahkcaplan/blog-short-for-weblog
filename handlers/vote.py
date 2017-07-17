from utils import Utils
from base import BaseHandler
from models.user import User
from models.post import Post

# Handler for liking post
class VoteUpPost(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id):
        post = Post.post_query(post_id)
        uid = int(self.read_secure_cookie('user_id'))

        # if uid not in post.liked_by:

        if self.user and self.user != post.author:
            post.liked_by += [uid]
            post.put()
            self.redirect("/blog/%s" % str(post.key().id()))

        else:
            self.redirect('/signup')

# Handler for disliking post
class VoteDownPost(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id):
        post = Post.post_query(post_id)
        if self.user and self.user != post.author:
            uid = int(self.read_secure_cookie('user_id'))

            liked_by_position = post.liked_by.index(uid)
            del post.liked_by[liked_by_position]

            post.put()

            self.redirect("/blog/%s" % str(post.key().id()))
        else:
            self.redirect('/signup')