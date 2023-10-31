from flask import Flask, request,render_template,flash, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stutech.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)

    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))
    role = db.Column(db.String())
    password = db.Column(db.String(200))

    def __init__(self,email,password, phone, address,name,role):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.password=password
        self.role=role

    def check_role(self):
        return self.role
    def check_password(self,password):
        return password


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        phone =  request.form['phone']
        address =  request.form['address']
        password = request.form['password']
        role=request.form['role']

        new_user = User(name=name,email=email, phone=phone, address=address,password=password,role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()


        if user and user.check_password(password) and user.role=='student':
            session['email'] = user.email
            return render_template('main.html')
        elif user and user.check_password(password) and user.role=='teacher':
            session['email'] = user.email
            return "render_template('dashboard.html')"
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/main')
def base():
    return render_template('main.html')

@app.route('/main2')
def xc():
    return render_template('main.html')

@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

@app.route("/main2")
def hai():
    return render_template("main.html")

@app.route('/update', methods=['GET','POST'])
def update():

    if request.method == 'POST':
        my_data=User.query.get(request.form.get('id'))


        my_data.name=request.form['name']
        my_data.address=request.form['address']
        my_data.email=request.form['email']
        my_data.phone=request.form['phone']
        my_data.role=User.query.get(request.form.get('role'))
        my_data.password =User.query.get(request.form.get('password'))


        db.session.commit()

        flash(" updated Successfully")
    return render_template('main.html')





if __name__ == '__main__':
    app.run(debug=True)