from google.appengine.ext import db

# Blog Post Entity
class Post(db.Model):
    author = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    liked_by = db.ListProperty(int)

    @classmethod
    def post_query(cls, post_id):
        post_key = db.Key.from_path('Post', int(post_id),
                                    parent=blog_key())
        post = db.get(post_key)
        return post

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)