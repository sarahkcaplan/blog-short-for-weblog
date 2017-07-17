from base import BaseHandler
from blog.models.user import User
from blog.models.comments import Comments
import utils

# Handler for adding a comment to a post.
class NewComment(BaseHandler):
    def get(self, post_id):
        if self.user:
            self.render('newcomment.html', post_id=post_id)

        else:
            self.redirect('/signup')

    def post(self, post_id):
        if self.user:
            content = self.request.get("content")

            if content:
                uid = int(self.read_secure_cookie('user_id'))
                user = User.by_id(uid)
                author = str(user.name)

                comment = Comments(parent=comment_key(), author=author,
                                   content=content, post_id=post_id)
                comment.put()
                comment_id = comment.key().id()

                self.redirect("/blog/%s/%s" % (post_id, comment_id))

            else:
                error = "Comment needs content"
                self.render('newcomment.html', error=error, post_id=post_id)
        else:
            self.redirect('/signup')


# Handler for Comment's permalink page
class CommentPage(BaseHandler):
    def get(self, post_id, comment_id):
        if self.user:

            self.render("comment.html", comment=comment, post_id=post_id,
                        comment_id=comment_id)
        else:
            self.redirect('/signup')


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

# Handler for deleteing a comment
class DeleteComment(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id, comment_id):
        comment = Comment.comment_query(comment_id)

        if self.user and self.user == comment.author:

            comment.delete()

            self.redirect("/blog/%s" % str(post_id))

        else:
            self.redirect('/signup')

