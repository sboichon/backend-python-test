from alayatodo import app, db
from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session
    )
from functools import wraps

from .models import User, Todo

TODO_PER_PAGE = 6


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('You need to be logged in')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = user.to_dict()
        session['logged_in'] = True
        return redirect('/todos/')

    flash('Wrong username / password')
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if not todo:
        flash('Todo id=%s doesn\'t exist' % id)
        return redirect('/todos/')
    return render_template('todo.html', todo=todo)


@app.route('/todo/<id>/json', methods=['GET'])
@login_required
def todo_json(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if not todo:
        flash('Todo id=%s doesn\'t exist' % id)
        return redirect('/todos/')
    return jsonify(todo.to_dict())


@app.route('/todo/<id>/complete', methods=['POST'])
@login_required
def todo_complete(id):
    is_completed = request.form.get('is_completed')
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()

    if not todo:
        flash('Todo id=%s doesn\'t exist' % id)
        return redirect('/todos/')

    if is_completed is not None:
        todo.is_completed = True
    else:
        todo.is_completed = False

    db.session.commit()

    return render_template('todo.html', todo=todo)


@app.route('/todos/', defaults={'page': 1}, methods=['GET'])
@app.route('/todos/<int:page>/', methods=['GET'])
@login_required
def todos(page):
    todos = Todo.query.filter_by(
        user_id=session['user']['id']).paginate(page, TODO_PER_PAGE)
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    if request.form.get('description', '') == '':
        flash("You need to provide a description")
        return redirect('/todos/')

    todo = Todo(user_id=session['user']['id'],
                description=request.form['description'])
    db.session.add(todo)
    db.session.commit()
    return redirect('/todos/')


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect('/todos/')
