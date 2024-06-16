from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models.task import Task
from app.models.user import User
from app import db,config
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# =========================================
# CRUD
# =========================================

@main.route('/add', methods=['POST'])
def add_task():
    task_title = request.form.get('title')
    task_description = request.form.get('description')
    task_done = request.form.get('done')
    task_favorite = request.form.get('favorite')

    new_task = Task()
    
    new_task.title = task_title
    new_task.done = task_done
    new_task.favorite = task_favorite
    new_task.creator_id = session['user_id']

    if task_description:
        new_task.description = task_description

    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.done = request.form.get('done') == 'true'
    task.favorite = request.form.get('favorite') == 'true'
    db.session.merge(task)
    db.session.commit()
    return redirect(url_for('main.index'))

# =========================================
# Login Signup
# =========================================
@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=user_name).first()

        if user and check_password_hash(user.password,password):
            print('login success')
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash('ユーザー名またはパスワードが間違っています')
    return render_template('login.html')

@main.route('/logout')
def logout():
    print('logout')
    # session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('ログアウトしました')
    return redirect(url_for('main.index'))

@main.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user:
            print('User already exists')
            return redirect(url_for('main.signup'))
        
        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.password = generate_password_hash(password, method='sha256')

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        redirect(url_for('main.index'))
    return render_template('signup.html')

# =========================================
#  routes
# =========================================
@main.route('/')
def index():
    tasks = Task.query.all()
    for task in tasks:
        user = User.query.filter_by(id=task.creator_id).first()
        task.creator_name = user.username if user else "Unknown"
    
    if session.get('user_id'):
        user = User.query.filter_by(id=session['user_id']).first()
        # print(user.username)
        return render_template('index.html', tasks=tasks, user_name=user.username)

    return render_template('index.html', tasks=tasks)

@main.route('/<int:task_id>/edit/', methods=['GET'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    print(task)
    return render_template('edit.html', task=task)

@main.route('/add', methods=['GET'])
def show_add_task():
    return render_template('add.html')

@main.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@main.route('/signup', methods=['GET'])
def show_signup():
    print('signup')
    return render_template('signup.html')


