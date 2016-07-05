from flask_testing import TestCase

from alayatodo import app, db


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('alayatodo.config.TestingConfig')
        self.db = db
        self.app = app
        return app

    def setUp(self):
        import ipdb; ipdb.set_trace()
        db.create_all()

    def tearDown(self):
        import ipdb; ipdb.set_trace()
        db.session.remove()
        db.drop_all()

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
