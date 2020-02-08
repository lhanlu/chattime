from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    jsonify
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Contact, Message

import random
import string

import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

engine = create_engine('sqlite:///chattime.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/users/')
def restaurants():
    session = DBSession()
    restaurants = session.query(User).all()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>/contact')
@app.route('/<int:user_id>/')
def contact(user_id):
    """
   This is a function to show contacts
    Args:
        user_id (data type: Integer):
                    the user id those contacts belongs to
    Returns:
     contact page
    """
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    contacts = session.query(Contact).filter_by(user_id=user_id)
    if contacts is None:
        return "You currently have no contacts"
    else:
        return render_template('contact.html', user=user,
                        contacts=contacts)


@app.route('/new', methods=['GET','POST'])
@app.route('/users/new', methods=['GET','POST'])
def newUser():
    """
   This is a function to add new user
    Returns:
        if the restaurant is created successfully, 
            return to users page and show message:New user created!
        else return to users page and show no message.
    """
    session = DBSession()
    if request.method == 'POST':
        newUser = User(name=request.form['name'],email=request.form['email'])
        session.add(newUser)
        session.commit()
        flash('New User %s created!' % newUser.name)
        return redirect(url_for('users'))
    else:
        return render_template('newUser.html')

@app.route('/<int:user_id>/new/', methods=['GET','POST'])
@app.route('/<int:user_id>/contact/new/', methods=['GET','POST'])
@app.route('/users/<int:user_id>/contact/new/', methods=['GET','POST'])
def newContact(user_id):
    """
   This is a function to add new contact
    Args:
        user_id (data type: Integer):
                    the user id that contact belongs to
    Returns:
        if the contact is created successfully,
            return to message page and show message:New contact created!
        else return to contact menu page and show no message.
    """
    session = DBSession()
    if request.method == 'POST':
        newContact = Contact(name=request.form['name'],
                            email=request.form['email'],
                            user_id=user_id)
        session.add(newContact)
        session.commit()
        flash("New contact created!")
        return redirect(url_for('contact', user_id = user_id))
    else:
        return render_template('newContact.html', user_id = user_id)


@app.route('/<int:user_id>/edit/', methods=['GET','POST'])
@app.route('/users/<int:user_id>/edit/', methods=['GET','POST'])
def editUser(user_id):
    """
   This is a function to edit exited user
    Args:
        user_id (data type: Integer):
                    the user id
    Returns:
        if the user infomation is edited successfully,
            return to user page and show message: User was edited!
        else return to editUser page and show no message.
    """
    session = DBSession()
    editedUser = session.query(User).filter_by(id=user_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedUser.name = request.form['name']
        if request.form['email']:
            editedUser.name = request.form['email']
        session.add(editedUser)
        session.commit()
        flash("User was edited!")
        return redirect(url_for('users'))
    else:
        return render_template('editUser.html', user=editedUser)



@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', 
        methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    """
   This is a function to add new menu item
    Args:
        restaurant_id (data type: Integer): 
                    the restaurant id that menu belongs to 
        menu-id(data type: Integer):
                    the menu id
    Returns:
        if the menu item is edited successfully, 
            return to restaurant menu page and show message:menu item was edited!
        else return to restaurant menu page and show no message.
    """
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if editedItem.user_id == login_session['user_id']:
        if request.method == 'POST':
            if request.form['name']:
                editedItem.name=request.form['name']
            if request.form['description']:
                editedItem.description=request.form['description']
            if request.form['price']:
                editedItem.price = request.form['price']
            if request.form['course']:
                editedItem.course = request.form['course']
            session.add(editedItem)
            session.commit()
            flash("Menu item was edited!")
            return redirect(url_for('restaurantMenu', 
                        restaurant_id=restaurant_id))
        else:
            return render_template('editmenuitem.html', 
                                    restaurant_id=restaurant_id, 
                                    menu_id=menu_id, item=editedItem)
    else:
        flash("You are not allowed to edit this menu item.")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    """
   This is a function to add new menu item
    Args:
        restaurant_id (data type: Integer): 
                    the restaurant id
    Returns:
        if the restaurant is deleted successfully, 
            return to restaurant page and show message:Restaurant was deleted!
        else return to restaurant page and show no message.
    """
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    deletedRes = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if deletedRes.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(deletedRes)
            session.commit()
            flash("Restaurant was deleted!")
            return redirect(url_for('restaurants'))
        else:
            return render_template('deleteRestaurant.html', 
                        restaurant=deletedRes)
    else:
        flash("You are not allowed to delete this restaurant.")
        return redirect(url_for('restaurants'))


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', 
            methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    """
   This is a function to add new menu item
    Args:
        restaurant_id (data type: Integer): 
                    the restaurant id that menu belongs to
        menu_id(data type: Integer):
                    the menu id 
    Returns:
        if the menu item is deleted successfully, 
            return to restaurant menu page and show message:menu item was deleted!
        else return to restaurant menu page and show no message.
    """
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if deletedItem.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(deletedItem)
            session.commit()
            flash("Menu item was deleted!")
            return redirect(url_for('restaurantMenu', 
                            restaurant_id=restaurant_id))
        else:
            return render_template('deletemenuitem.html', item=deletedItem)
    else:
        flash("You are not allowed to delete this menu item.")
        return redirect(url_for('restaurantMenu', 
                                restaurant_id=restaurant_id))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
