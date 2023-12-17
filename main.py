from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone, timedelta
import pytz

app = Flask(__name__)

class Task:
    def __init__(self, id, content, date_created):
        self.id = id
        self.content = content
        self.date_created = date_created
        self.last_updated = None  # Yeni eklenen özellik

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
        # GET isteği için boş bir form göster
        return render_template('add.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        if request.method == 'POST':
            task.content = request.form.get('content')
            task.last_updated = datetime.utcnow().replace(tzinfo=pytz.utc)
            return redirect(url_for('index'))
        else:
            task.date_local = task.date_created.astimezone(timezone(timedelta(hours=3)))  # GMT+3 için
            return render_template('edit.html', task=task)
    else:
        return 'Task not found', 404

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
