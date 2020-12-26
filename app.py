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
    return redirect('/users')

@app.route('/users', methods=["GET"])
def list_users():
    users = Users.query.all()
    return render_template('base.html', users=users)

@app.route('/users/new', methods=["GET"])
def present_form():
    return render_template('form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = Users(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:id>')
def profile(id):
    user = Users.query.get_or_404(id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:id>/edit', methods=["GET"])
def get_edit(id):
    user = Users.query.get_or_404(id)
    return render_template('profile_edit.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def update_user(id):
    user = Users.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{id}')

@app.route('/users/<int:id>/delete')
def delete_user(id):
    Users.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')