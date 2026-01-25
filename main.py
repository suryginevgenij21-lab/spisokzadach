from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'db.sqlite3')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT id, description, completed FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (description, completed) VALUES (?, ?)', (description, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db_connection()
    # переключить статус
    task = conn.execute('SELECT completed FROM tasks WHERE id=?', (id,)).fetchone()
    new_status = 0 if task['completed'] else 1
    conn.execute('UPDATE tasks SET completed=? WHERE id=?', (new_status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Новое: Редактирование задачи ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    if request.method == 'POST':
        new_desc = request.form['description']
        conn.execute('UPDATE tasks SET description=? WHERE id=?', (new_desc, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        task = conn.execute('SELECT * FROM tasks WHERE id=?', (id,)).fetchone()
        conn.close()
        return render_template('edit.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)