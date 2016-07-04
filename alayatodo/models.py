from alayatodo import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def to_dict(self):
        return {c.name: str(getattr(self, c.name))
                for c in self.__table__.columns}


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    description = db.Column(db.String, nullable=False)
    is_completed = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref=db.backref("todos", order_by=id))

    def __init__(self, user_id, description, is_completed=False):
        self.user_id = user_id
        self.description = description
        self.is_completed = is_completed

    def __repr__(self):
        return '<Todo {0}>'.format(self.description)
