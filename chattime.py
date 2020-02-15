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
from database_setup import User, Contact, Message, Base

import random
import string

import httplib2
import json
from flask import make_response
import requests

from datetime import datetime


app = Flask(__name__)

engine = create_engine('sqlite:///chattime.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/JSON')
@app.route('/users/JSON')
def userJSON():
    session = DBSession()
    users = session.query(User).all()
    return jsonify(User=[u.serialize for u in users])


@app.route('/users/<int:user_id>/contact/JSON')
@app.route('/<int:user_id>/contact/JSON')
def contactJSON(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    contacts = session.query(Contact).filter_by(user_id=user.id).all()
    return jsonify(Contact=[c.serialize for c in contacts])

@app.route('/<int:user_id>/contact/<int:contact_id>/JSON')
@app.route('/users/<int:user_id>/<int:contact_id>/JSON')
@app.route('/users/<int:user_id>/contact/<int:contact_id>/JSON')
def messageJSON(user_id,contact_id):
    session = DBSession()
    messages = session.query(Message).filter_by(user_id=user_id, contact_id=contact_id).all()
    return jsonify(Message=[m.serialize for m in messages])


@app.route('/')
@app.route('/users/')
def users():
    session = DBSession()
    users = session.query(User).all()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>/contact')
@app.route('/users/<int:user_id>/')
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
        else return to editUser page and show no message.b
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



@app.route('/<int:user_id>/<int:contact_id>/edit/',
        methods=['GET','POST'])
@app.route('/users/<int:user_id>/<int:contact_id>/edit/',
        methods=['GET','POST'])
@app.route('/<int:user_id>/contact/<int:contact_id>/edit/',
        methods=['GET','POST'])
@app.route('/users/<int:user_id>/contact/<int:contact_id>/edit/',
        methods=['GET','POST'])
def editContact(user_id, contact_id):
    """
   This is a function to edit contact
    Args:
        user_id (data type: Integer):
                    the user id that contact belongs to
        contact_id(data type: Integer):
                    the contact id
    Returns:
        if the contact item is edited successfully,
            return to contact page and show message:contact was edited!
        else return to contact page and show no message.
    """
    session = DBSession()
    editedCon = session.query(Contact).filter_by(id=contact_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCon.name=request.form['name']
        if request.form['email']:
            editedCon.name=request.form['email']
        session.add(editedCon)
        session.commit()
        flash("Contact was edited!")
        return redirect(url_for('contact',
                    user_id=user_id))
    else:
        return render_template('editContact.html',
                                user_id=user_id,
                                contact_id=contact_id, contact=editedCon)


@app.route('/<int:user_id>/delete/', methods=['GET','POST'])
@app.route('/users/<int:user_id>/delete/', methods=['GET','POST'])
def deleteUser(user_id):
    """
   This is a function to delete user
    Args:
        user_id (data type: Integer):
                    the user id
    Returns:
        if the user is deleted successfully,
            return to user page and show message:User was deleted!
        else return to user page and show no message.
    """
    session = DBSession()
    deletedUser = session.query(User).filter_by(id=user_id).one()
    if request.method == 'POST':
        session.delete(deletedUser)
        session.commit()
        flash("User was deleted!")
        return redirect(url_for('users'))
    else:
        return render_template('deleteUser.html',
                    user=deletedUser)



@app.route('/<int:user_id>/<int:contact_id>/delete/',
methods=['GET','POST'])
@app.route('/users/<int:user_id>/<int:contact_id>/delete/',
        methods=['GET','POST'])
@app.route('/<int:user_id>/contact/<int:contact_id>/delete/',
        methods=['GET','POST'])
@app.route('/users/<int:user_id>/contact/<int:contact_id>/delete/',
            methods=['GET','POST'])
def deleteContact(user_id, contact_id):
    """
   This is a function to delete contact
    Args:
        user_id (data type: Integer):
                    the user id that contact belongs to
        contact_id(data type: Integer):
                    the contact id
    Returns:
        if the contact is deleted successfully,
            return to contact page and show message:contact was deleted!
        else return to contact page and show no message.
    """
    session = DBSession()
    deletedCon = session.query(Contact).filter_by(id=contact_id).one()
    if request.method == 'POST':
        session.delete(deletedCon)
        session.commit()
        flash("Contact was deleted!")
        return redirect(url_for('contact',
                        user_id=user_id))
    else:
        return render_template('deleteContact.html', contact=deletedCon)

@app.route('/<int:user_id>/<int:contact_id>/message/')
@app.route('/<int:user_id>/contact/<int:contact_id>/message/')
@app.route('/users/<int:user_id>/<int:contact_id>/message/new/')
@app.route('/users/<int:user_id>/contact/<int:contact_id>/message/')
def message(user_id, contact_id):
    """
   This is a function to show message
    Args:
        user_id (data type: Integer):
                    the user id those contacts belongs to
        contact_id (data type: Integer):
                    the contact id that contacts belongs to
    Returns:
     Message page
    """
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    contact = session.query(Contact).filter_by(id = contact_id, user_id = user_id).one()
    messages = session.query(Message).filter_by(contact_id=contact_id, user_id=user_id)
    r_messages = session.query(Message).filter_by(user_id=contact_id, contact_id=user_id)
    if messages and r_messages is None:
        return "You currently have no messages with this contact"
    else:
        return render_template('message.html', user=user,
                        contact = contact, messages=messages, r_messages = r_messages)


@app.route('/<int:user_id>/<int:contact_id>/message/new/', methods=['GET','POST'])
@app.route('/<int:user_id>/contact/<int:contact_id>/message/new/', methods=['GET','POST'])
@app.route('/users/<int:user_id>/<int:contact_id>/message/new/', methods=['GET','POST'])
@app.route('/users/<int:user_id>/contact/<int:contact_id>/message/new/', methods=['GET','POST'])
def sendMessage(user_id, contact_id):
    """
   This is a function to send message
    Args:
        user_id (data type: Integer):
                    the user id that user belongs to
        contact_id (data type: Integer):
                    the contact id that contact belongs to
    Returns:
            return to message page and show all the message
        else return to contact page and show no message.
    """
    session = DBSession()
    if request.method == 'POST':
        newMessage = Message(content=request.form['content'],
                            time=datetime.now(),
                            contact_id = contact_id,
                            user_id=user_id,)
        session.add(newMessage)
        session.commit()
        flash("Message sent!")
        return redirect(url_for('message', user_id = user_id, contact_id = contact_id))
    else:
        return render_template('sendMessage.html', user_id = user_id, contact_id = contact_id)

    


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
