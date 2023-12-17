from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone, timedelta
import pytz

app = Flask(__name__)

class Task:
    def __init__(self, id, content, date_created, completed=False):
        self.id = id
        self.content = content
        self.date_created = date_created
        self.last_updated = None
        self.completed = completed

tasks = [
    Task(1, "Task 1", datetime(2023, 12, 17, 17, 0, 0, tzinfo=timezone.utc)),
    # Diğer görevler...
]

@app.route('/')
def index():
    for task in tasks:
        task.date_local = task.date_created.astimezone(timezone(timedelta(hours=3)))  # GMT+3 için
        task.last_updated_local = task.last_updated.astimezone(timezone(timedelta(hours=3))) if task.last_updated else None

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        content = request.form.get('content')
        new_task = Task(id=len(tasks) + 1, content=content, date_created=datetime.utcnow().replace(tzinfo=pytz.utc))
        tasks.append(new_task)
        return redirect(url_for('index'))
    else:
        return render_template('add.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task and not task.completed:
        if request.method == 'POST':
            task.content = request.form.get('content')
            task.last_updated = datetime.utcnow().replace(tzinfo=pytz.utc)
            return redirect(url_for('index'))
        else:
            task.date_local = task.date_created.astimezone(timezone(timedelta(hours=3)))  # GMT+3 için
            return render_template('edit.html', task=task)
    else:
        return 'Task not found or completed', 404

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        task.completed = not task.completed
        return redirect(url_for('index'))
    else:
        return 'Task not found', 404

if __name__ == '__main__':
    app.run(debug=True)
