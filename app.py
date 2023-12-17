from flask import Flask, render_template
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

class Task:
    def __init__(self, id, content, date_created):
        self.id = id
        self.content = content
        self.date_created = date_created
        self.date_local = date_created.astimezone(timezone(timedelta(hours=3)))  # GMT+3 için

# Örnek bir görev listesi
tasks = [
    Task(1, "Task 1", datetime(2023, 12, 17, 17, 0, 0, tzinfo=timezone.utc)),
    # Diğer görevler...
]

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
