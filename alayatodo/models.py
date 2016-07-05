from alayatodo import db


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def to_dict(self):
        return {c.name: str(getattr(self, c.name))
                for c in self.__table__.columns}


class User(CRUDMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Todo(CRUDMixin, db.Model):
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
