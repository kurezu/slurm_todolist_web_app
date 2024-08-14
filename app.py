from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost/testdb2'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    create_time = db.Column(db.DateTime)
    close_time = db.Column(db.DateTime, nullable=True)
    
    def get_close_time(self):
        return self.close_time.strftime('%d.%m.%Y %H:%M:%S')
    
    def get_create_time(self):
        return self.create_time.strftime('%d.%m.%Y %H:%M:%S')


@app.route('/')
def index():
    return render_template('base.html', tasks=Task.query.order_by(Task.id).all())

@app.route('/add', methods=["POST"])
def add():
    text = request.form.get('task')
    details = request.form.get('details')
    db.session.add(
        Task(text=text, details=details, create_time = datetime.today())
    )
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear', methods=["POST"])
def clear():
    Task.query.delete()    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def done(task_id):
    try:
        task = Task.query.get(task_id)
        task.is_done = True 
    except AttributeError:
        flash(f'Задание с номером {task_id} не найдено.', 'success')
        return redirect(url_for('index'))
    flash(f'Задание с номером {task_id} завершено.', 'success')
    task.close_time = datetime.today()
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reopen/<int:task_id>')
def reopen(task_id):
    try:
        task = Task.query.get(task_id)   
        task.is_done = False 
    except AttributeError:
        flash(f'Задание с номером {task_id} не найдено.', 'success')
        return redirect(url_for('index'))
    flash(f'Задание с номером {task_id} переоткрыто.', 'success')
    task.close_time = None
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context(): db.create_all()
    app.run(debug=True)
    
