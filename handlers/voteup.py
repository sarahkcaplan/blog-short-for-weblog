import utils
from base import BaseHandler

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