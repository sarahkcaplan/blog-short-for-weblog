import utils
from base import BaseHandler

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