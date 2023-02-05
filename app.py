from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    complete = db.Column(db.Boolean)
    data_created = db.Column(db.DateTime , default =datetime.utcnow)

app.app_context().push()
@app.route('/')
def index():
    #show all todos
    todo_list = Todo.query.order_by(Todo.data_created).all()
    print(todo_list)
    return render_template('base.html',todo_list = todo_list)

@app.route('/add',methods = ["POST",'GET'])
def add():
    #add new item
    title = request.form.get('title')
    new_todo = Todo(title=title,complete=False) 
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))#redirect user to main page

@app.route('/update/<int:todo_id>')#gotta know what exact item to update
def update(todo_id):
    #add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))#redirect user to main page
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    #add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)#allows not reload server everytime