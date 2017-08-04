from datetime import datetime

from blog_app.database import db


class Article(db.Model):
    id = db.Column(db.Integer, primery_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, content, category, pub_date=None):
        self.title = title
        self.content = content
        self.category = category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Article %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primery_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name