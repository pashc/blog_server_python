from datetime import datetime
import time
from blog_app.database import db

ARTICLE_ID = db.Sequence('article_id_seq', start=0)


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, server_default=ARTICLE_ID.next_value())
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('articles', lazy='dynamic'))

    def to_dict(self):
        return dict(id=self.id,
                    title=self.title,
                    content=self.content,
                    pub_date=time.mktime(self.pub_date.timetuple()),
                    category=self.category.name if self.category else None)

    def __init__(self, title, content, category, pub_date=None):
        self.title = title
        self.content = content
        self.category = category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Article %r>' % self.title
