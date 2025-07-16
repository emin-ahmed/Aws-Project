from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'project1-stack-database-lyafsiemdzet.cje00guwyyb6.eu-north-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'StrongPwd123!',
    'database': 'appdb'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        desc = request.form['description']
        conn = mysql.connector.connect(**DB_CONFIG)
        c = conn.cursor()
        c.execute('INSERT INTO tasks (description) VALUES (%s)', (desc,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = mysql.connector.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute('SELECT id, description, done FROM tasks')
    tasks = c.fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks)

@app.route('/done/<int:task_id>')
def mark_done(task_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute('UPDATE tasks SET done = 1 WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

