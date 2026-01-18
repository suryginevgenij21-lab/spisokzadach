import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask("name")

# Абсолютный путь к базе данных
DB_PATH = r"C:\Users\Oleg\PycharmProjects\PythonProjecexp\db.sqlite3"

# Создаем папку для базы данных, если нужно
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    description = request.form.get('description')
    if description:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (description, completed) VALUES (?, ?)', (description, False))
            conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
        current = cursor.fetchone()
        if current:
            new_status = not current[0]
            cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, task_id))
            conn.commit()
    return redirect(url_for('index'))


if "name" == 'main':
    init_db()
    app.run(debug=True)