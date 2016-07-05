from flask import url_for

from alayatodo.tests.test_base import BaseTestCase
from alayatodo.models import Todo


class TodoViewsTests(BaseTestCase):

    def test_get_todo(self):
        self.request_as_logged_in_user(self.user_1,
                                       url_for('todo', id=self.todo_1.id),
                                       'GET')
        self.assert_template_used('todo.html')
        self.assert_context("todo", self.todo_1)

    def test_get_todos(self):
        self.request_as_logged_in_user(self.user_1,
                                       url_for('todos'),
                                       'GET')
        self.assert_template_used('todos.html')
        self.assert_context("todos", [self.todo_1])

    def test_get_todo_json(self):
        response = self.request_as_logged_in_user(
            self.user_1,
            url_for('todo_json', id=self.todo_1.id),
            'GET')
        self.assertEquals(response.json, self.todo_1.to_dict())

    def test_get_todo_of_another_user_should_return_not_found(self):
        response = self.request_as_logged_in_user(
            self.user_1,
            url_for('todo', id=self.todo_2.id),
            'GET')
        self.assert_redirects(response, url_for('todos'))

    def test_create_todo(self):
        response = self.request_as_logged_in_user(
            self.user_1,
            url_for('todos_POST'),
            'POST',
            data={'description': 'bonjour'})
        self.assert_redirects(response, url_for('todos'))

        self.assertIsNotNone(
            Todo.query.filter_by(description='bonjour').first())

    def test_complete_todo(self):
        self.request_as_logged_in_user(
            self.user_1,
            url_for('todo_complete', id=self.todo_1.id),
            'POST',
            data={'is_completed': 1})

        self.assert_template_used('todo.html')
        self.assert_context("todo", self.todo_1)
        self.assertTrue(self.todo_1.is_completed)

        self.request_as_logged_in_user(
            self.user_1,
            url_for('todo_complete', id=self.todo_1.id),
            'POST',
            data={})

        self.assert_template_used('todo.html')
        self.assert_context("todo", self.todo_1)
        self.assertFalse(self.todo_1.is_completed)

    def test_delete_todo(self):
        response = self.request_as_logged_in_user(
            self.user_1,
            url_for('todo_delete', id=self.todo_1.id),
            'POST')
        self.assert_redirects(response, url_for('todos'))
        self.assertIsNone(
            Todo.query.filter_by(id=self.todo_1.id).first())

    def test_todo_views_unaccesible_when_not_logged_in(self):
        response = self.client.get(url_for('todo', id=self.todo_1.id))
        self.assert_redirects(response, url_for('login'))

        response = self.client.get(url_for('todo_json', id=self.todo_1.id))
        self.assert_redirects(response, url_for('login'))

        response = self.client.get(url_for('todos'))
        self.assert_redirects(response, url_for('login'))

        response = self.client.post(url_for('todos_POST',
                                    data={'description': 'poipoi'}))
        self.assert_redirects(response, url_for('login'))

        response = self.client.post(url_for('todo_complete', id=self.todo_1.id),
                                    data={'is_completed': 1})
        self.assert_redirects(response, url_for('login'))

        response = self.client.post(url_for('todo_delete', id=self.todo_1.id))
        self.assert_redirects(response, url_for('login'))
