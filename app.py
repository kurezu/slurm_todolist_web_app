from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost/testdb'
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)


@app.route('/')
def index():
    return render_template('base.html', tasks=Task.query.order_by(Task.id).all())

@app.route('/add', methods=["POST"])
def add():
    text = request.form.get('task')
    db.session.add(
        Task(text=text)
    )
    print (text)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear', methods=["POST"])
def clear():
    Task.query.delete()    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def done(task_id):
    task = Task.query.get(task_id)   
    task.is_done = True 
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    
