import utils
from base import BaseHandler

# Handler for editing a comment
class EditComment(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id, comment_id):
        comment = Comment.comment_query(comment_id)
        if self.user and self.user == comment.author:
            content = comment.content
            self.render('editcomment.html', post_id=post_id,
                        comment_id=comment_id, content=content)

        else:
            self.redirect('/signup')

    def post(self, post_id, comment_id):
        comment = Comment.comment_query(comment_id)
        if self.user and self.user == comment.author:
            content = self.request.get("content")

            if content:
                comment.content = content
                comment.put()
                self.redirect("/blog/%s" % str(post_id))

            else:
                error = "We need a comment"
                self.render('editcomment.html', error=error, post_id=post_id,
                            comment_id=comment_id, content=content)
        else:
            self.redirect('/signup')