from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

class Task:
    def __init__(self, id, content, date_created):
        self.id = id
        self.content = content
        self.date_created = date_created

# Örnek bir görev listesi
tasks = [
    Task(1, "Task 1", datetime(2023, 12, 17, 17, 0, 0, tzinfo=timezone.utc)),
    # Diğer görevler...
]

@app.route('/')
def index():
    # Her bir görevin UTC'den yerel saate dönüştürülmesi
    for task in tasks:
        task.date_local = task.date_created.astimezone(timezone(timedelta(hours=3)))  # GMT+3 için

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    new_task = Task(id=len(tasks) + 1, content=content, date_created=datetime.utcnow())
    tasks.append(new_task)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>')
def edit(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        task.date_local = task.date_created.astimezone(timezone(timedelta(hours=3)))  # GMT+3 için
        return render_template('edit.html', task=task)
    else:
        return 'Task not found', 404

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        task.content = request.form.get('content')
        task.date_created = datetime.utcnow()
        return redirect(url_for('index'))
    else:
        return 'Task not found', 404

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
