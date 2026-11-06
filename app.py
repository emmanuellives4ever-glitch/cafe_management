from flask import Flask, render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'emerjemrj'


#models

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    info=db.Column(db.String(500),nullable=True)
    image = db.Column(db.String(200), nullable=False)  #filename only



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=True)
    contact=db.Column(db.Integer,nullable=True)
    password= db.Column(db.String(120), nullable=False)


#forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,ValidationError
from wtforms.validators import DataRequired, Length, Email,EqualTo,Optional

class LoginForm(FlaskForm):
    identifier = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    
        

    username = StringField(label='User Name', validators=[Length(min=2, max=20)])
    email_address = StringField(label='Email Address', validators=[ ])
    contact = StringField("Contact", validators=[Length(max=30), Optional()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    
    submit = SubmitField(label='Submit')



def seed_menu():
    if MenuItem.query.count() == 0:   # only add if the table is empty
        items = [
            #beverages
            MenuItem(name="Cold Coffee", category="Beverages", price=159, image="coffee.jpg"),
            MenuItem(name="Americano", category="Beverages", price=117, image="americano.jpg"),
            MenuItem(name="Espresso", category="Beverages", price=98, image="espresso.jpg"),
            MenuItem(name="Frappuccino", category="Beverages", price=189, image="frapee.jpg"),
            MenuItem(name="Flat White", category="Beverages", price=179, image="flatwhite.jpg"),
            MenuItem(name="Java Chip ", category="Beverages", price=216, image="javachip.jpg"),
            #cakes
            MenuItem(name="Red Velvet Cake", category="Cakes", price=689, image="pastries.jpeg"),
            MenuItem(name="Eggless Pineapple cake", category="Cakes", price=458, image="pinapple.jpg"),
            MenuItem(name="Dutch Truffle cake ", category="Cakes", price=657, image="dutch.jpg"),
            MenuItem(name="Dark choclate cake", category="Cakes", price=450, image="dutch.jpg"),
            MenuItem(name="Hazelnut cake ", category="Cakes", price=879, image="hazelnut.jpeg"),
            MenuItem(name="Pinapple Cake", category="Cakes", price=346, image="pinapple.jpg"),

            #bread
            MenuItem(name="Sourdough Bread", category="Breads", price=120, image="breads.jpeg"),
            MenuItem(name="Milk Bread", category="Breads", price=120, image="milk.jpeg"),
            MenuItem(name="Sandwich Bread", category="Breads", price=120, image="breads.jpeg"),

        ]
        db.session.add_all(items)
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_menu()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    items=MenuItem.query.all()
    return render_template('menu.html',items=items)




@app.route('/register',methods=["GET","POST"])
def register():
    form= RegisterForm()
    if form.validate_on_submit():
        user=User(username=form.username,
                  email_address=form.email_address.data.strip().lower(),
                  contact=form.contact.data,
                  password=form.password1)
        db.session.add(user)
        db.session.commit()

        flash("Redistered User","success")
        return redirect(url_for('index'))
    return render_template("register.html",form=form)




@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        flash("Login submitted", "success")
        return redirect(url_for('index'))
    return render_template('login.html', form=form)





if __name__ == '__main__':
    app.run(debug=True)