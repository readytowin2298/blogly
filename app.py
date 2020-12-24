"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    users = Users.query.all()
    return render_template('base.html', users=users)

@app.route('/add_user')
def present_form():
    return render_template('form.html')

@app.route('/form', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = Users(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f'/profile/{user.id}')

@app.route('/profile/<int:id>')
def profile(id):
    user = Users.query.get_or_404(id)
    return render_template('profile.html', user=user)