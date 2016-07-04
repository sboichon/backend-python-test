"""AlayaNotes."""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from alayatodo import app, db
from alayatodo.models import User, Todo


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def create_fixtures():
    """Creates the users."""
    db.session.add(User(username='user1', password='user1'))
    db.session.add(User(username='user2', password='user2'))
    db.session.add(User(username='user3', password='user3'))

    """ Creates the todos """
    db.session.add(Todo(description='Vivamus tempus', user_id=1))
    db.session.add(Todo(description='lorem ac odio', user_id=1))
    db.session.add(Todo(description='Ut congue odio', user_id=1))
    db.session.add(Todo(description='Sodales finibus', user_id=1))

    db.session.add(Todo(description='Lorem ipsum', user_id=3))
    db.session.add(Todo(description='In lacinia est', user_id=3))
    db.session.add(Todo(description='Odio varius gravida', user_id=3))

    db.session.commit()


if __name__ == '__main__':
    manager.run()
