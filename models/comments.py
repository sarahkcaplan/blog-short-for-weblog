from google.appengine.ext import db

# Comments Entity
class Comments(db.Model):
    author = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def comment_query(cls,comment_id):
        ccomment_key = db.Key.from_path('Comments', int(comment_id),
                                 parent=comment_key())
        comment = db.get(comment_key)
        return comment