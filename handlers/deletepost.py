import utils
from base import BaseHandler

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
