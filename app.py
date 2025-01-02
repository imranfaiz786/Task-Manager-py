from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite Database setup
def init_db():
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

# Home route to display tasks
@app.route('/')
def index():
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)', 
                   (title, description, False))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to update task status or information
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        done = bool(request.form.get('done'))
        cursor.execute('UPDATE tasks SET title = ?, description = ?, done = ? WHERE id = ?',
                       (title, description, done, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
    task = cursor.fetchone()
    conn.close()
    return render_template('update.html', task=task)

# Route to delete a task
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
