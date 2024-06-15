from flask import Blueprint, render_template, request, redirect, url_for
from app.models.task import Task
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    tasks = Task.query.all()
    print(tasks)
    return render_template('index.html', tasks=tasks)

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
    # if task:
    task.title = request.form.get('title')
    task.done = request.form.get('done', 'off') == 'on'
    task.done = request.form.get('done') == 'true'
    task.favorite = request.form.get('favorite') == 'true'
    db.session.merge(task)
    db.session.commit()
    return redirect(url_for('main.index'))

# =========================================
# 
# =========================================
@main.route('/<int:task_id>/edit/', methods=['GET'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    return render_template('edit.html', task=task)