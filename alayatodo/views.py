from alayatodo import app
from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session
    )
from functools import wraps

from .models import db, User, Todo


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
        return redirect('/todo')

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
    todo = Todo.query.filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo/<id>/json', methods=['GET'])
@login_required
def todo_json(id):
    todo = Todo.query.filter_by(id=id).first()
    return jsonify(todo.to_dict())


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    if request.form.get('description', '') == '':
        flash("You need to provide a description")
        return redirect('/todo')

    todo = Todo(user_id=session['user']['id'],
                description=request.form['description'])
    db.session.add(todo)
    db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect('/todo')
