from flask import url_for

from alayatodo.tests.test_base import BaseTestCase
from alayatodo.models import Todo, User


class TodoViewsTests(BaseTestCase):
    def setUp(self):
        self.user_1 = User('user7', 'pass1')
        self.user_2 = User('user8', 'pass2')
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

    def tearDown(self):
        self.db.session.delete(self.todo_1)
        self.db.session.delete(self.todo_2)
        self.db.session.commit()

        self.db.session.delete(self.user_1)
        self.db.session.delete(self.user_2)
        self.db.session.commit()

    def test_get_todo(self):
        self.request_as_logged_in_user(self.user_1,
                                       url_for('todo', id=self.todo_1.id),
                                       'GET')
        self.assert_template_used('todo.html')
        self.assert_context("todo", self.todo_1)

    def test_get_todo_of_another_user_should_return_not_found(self):
        response = self.request_as_logged_in_user(
            self.user_1,
            url_for('todo', id=self.todo_2.id),
            'GET')
        self.assert_redirects(response, url_for('todos'))

    def test_get_todo_not_logged_in(self):
        response = self.client.get(url_for('todo', id=self.todo_1.id))
        self.assert_redirects(response, url_for('login'))
