from passlib.apps import custom_app_context as pwd_context

from blog_app.database import db

USER_ID = db.Sequence('user_id_seq', start=0)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, USER_ID, primary_key=True, server_default=USER_ID.next_value())
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % self.username
