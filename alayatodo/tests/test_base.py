from flask_testing import TestCase

from alayatodo import app, db
from alayatodo.models import Todo, User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('alayatodo.config.TestingConfig')
        self.db = db
        self.app = app
        return app

    def setUp(self):
        self.db.create_all()
        try:
            self.setUpModels()
        except:
            # The tearDown is not run if the setUp crash
            self.db.session.remove()
            self.db.drop_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def setUpModels(self):
        self.user_1 = User('user1', 'pass1')
        self.user_2 = User('user2', 'pass2')
        self.db.session.add(self.user_1)
        self.db.session.add(self.user_2)
        self.db.session.commit()

        self.todo_1 = Todo(user_id=self.user_1.id,
                           description='hello')

        self.todo_2 = Todo(user_id=self.user_2.id,
                           description='hello !')
        self.db.session.add(self.todo_1)
        self.db.session.add(self.todo_2)
        self.db.session.commit()

    def tearDownModels(self):
        pass

    def request_as_logged_in_user(self, user, path, method='GET',
                                  *args, **kwargs):
        """Make an http request with a logged in user."""
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user'] = user.to_dict()
                sess['logged_in'] = True
            kwargs['method'] = method
            kwargs['path'] = path
            return c.open(*args, **kwargs)
