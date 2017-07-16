import utils
from base import BaseHandler

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