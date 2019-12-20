from flask import Flask, render_template, redirect, \
    request

from db import create_connection

app = Flask(__name__)


@app.route('/')
def hello_world():
    conn = create_connection('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todo')
    todos = cursor.fetchall()
    priority_choices = range(1, 6)
    context = {
        'todos': todos,
        'priority_choices': priority_choices
    }
    return render_template(
        'index.html', **context
    )


@app.route('/add-todo/', methods=['POST'])
def add_todo():
    text = request.form["todo-text"]
    priority = request.form["priority"]
    conn = create_connection('db.sqlite3')
    if len(text) and priority.isdigit() and 0 < int(priority) <= 5:
        cursor = conn.cursor()
        cursor.execute(
            f'INSERT INTO todo (text, priority)'
            f' VALUES ("{request.form["todo-text"]}", "{request.form["priority"]}")'
        )
        conn.commit()
    else:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todo')
        todos = cursor.fetchall()
        priority_choices = range(1, 6)
        context = {
            'error': True,
            'todos': todos,
            'priority_choices': priority_choices
        }
        return render_template(
            'index.html', **context
        )
    return redirect('/')


@app.route('/delete-todo/', methods=['POST'])
def delete_todo():
    conn = create_connection('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(
        f'DELETE FROM todo WHERE id={request.form["id"]}'
    )
    conn.commit()
    return redirect('/')


@app.route('/my_profile/')
def my_profile():
    return 'Hey! This is your profile'


if __name__ == '__main__':
    app.run(debug=True)
