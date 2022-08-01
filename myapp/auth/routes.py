import os
from urllib import response
from myapp.app import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..myhelper import myhelper
from ..model import mymodel

blueprint = Blueprint('auth', __name__)

model = mymodel.MySqlDb(mysql)

#Auth routes
@blueprint.route('/', methods=['GET'])
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = model.login(username, password)
        if result == 'success':
            return {
                'status': 'success',
                'message': 'Login successful',
                'token': session['auth_token']
            }
        elif result == 'password incorrect':
            return {
                'status': 'error',
                'message': 'Password incorrect'
            }
        else:
            return {
                'status': 'error',
                'message': 'User not found'
            }
       
    else:
        return render_template('pages/login/index.html')


#create account
@blueprint.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        fullname = request.form['fullname']
        password = request.form['password']

        hashed_password = myhelper.hashpassword(password)
        result = model.create_account(fullname, username, email, hashed_password)
        if result == 'success':
            return {
                'status': 'success',
                'message': 'Account created successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Account already exists'
            }
    else:
        return render_template('pages/create/index.html')

#forgot password
@blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        #verify email
        check_email = model.check_email(email)
        if check_email:
            verification_code = myhelper.random_digits(5)
            message = f'Hi, your password reset verification code is: {verification_code}'
            send_email =  myhelper.send_email(email, message)
            if send_email == 'success':
                return {
                    'status': 'success',
                    'message': 'Verification code sent to your email'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Something went wrong'
                }
        else:
            return {
                'status': 'error',
                'message': 'Email not found'
            }
    else:
        return render_template('pages/forgotpassword/index.html')

#user area
@blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    if 'auth_token' in session:
        user = session.get('username')
        user = model.get_user(user)
        tasks = model.get_tasks(user['username'])
        return render_template('pages/dashboard/index.html', user=user, tasks=tasks)
    else:
        return redirect(url_for('auth.login'))

#logout
@blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return {
        'status': 'success',
        'message': 'Logout successful'
    }

#edit user
@blueprint.route('/edit_user', methods=['GET', 'UPDATE'])
def edit_user():
    if 'auth_token' in session:
        if request.method == 'UPDATE':
            user = session.get('username')
            user = model.get_user(user)
            fullname = request.form['name']
            username = request.form['username']
            email = request.form['email']
            result = model.edit_user(user['id'], fullname, username, email)
            if result == 'success':
                return {
                    'status': 'success',
                    'message': 'User updated successfully'
                }
            elif result == 'account exists':
                return {
                    'status': 'error',
                    'message': 'Username already exists'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Something went wrong'
                }
        else:
            user = session.get('username')
            user = model.get_user(user)
            return render_template('pages/dashboard/edit.html', user=user)
    else:
        return redirect(url_for('auth.login'))
#delete user
@blueprint.route('/delete_user', methods=['DELETE'])
def delete_user():
    if 'auth_token' in session:
        user = session.get('username')
        user = model.get_user(user)
        result = model.delete_user(user['username'])
        if result == 'success':
            return {
                'status': 'success',
                'message': 'User deleted successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Something went wrong'
            }
    else:
        return redirect(url_for('auth.login'))


#add task
@blueprint.route('/add_task', methods=['POST', 'GET'])
def add_task():
    if 'auth_token' in session:
        user = session.get('username')
        user = model.get_user(user)
        if request.method == 'POST':
            task  = {
                'task': request.form['task'],
                'description': request.form['description'],
                'Category': request.form['Category'],
                'priority': request.form['priority']
            }
            result = model.add_task(user['username'], task)
            if result == 'success':
                return {
                    'status': 'success',
                    'message': 'Task added successfully'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Something went wrong',
                    'error': result
                }
        else:
            user = session.get('username')
            user = model.get_user(user)
            return render_template('pages/addtask/index.html', user=user)
    else:
        return redirect(url_for('auth.login'))

#delete task
@blueprint.route('/delete_task', methods=['DELETE'])
def delete_task():
    if 'auth_token' in session:
        user = session.get('username')
        user = model.get_user(user)
        task_id = request.form['id']
        result = model.delete_task(user['username'], task_id)
        if result == 'success':
            return {
                'status': 'success',
                'message': 'Task deleted successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Something went wrong'
            }
    else:
        return redirect(url_for('auth.login'))

#mark task as done
@blueprint.route('/mark_task', methods=['UPDATE'])
def mark_task():
    if 'auth_token' in session:
        user = session.get('username')
        user = model.get_user(user)
        task_id = request.form['id']
        result = model.mark_task(user['username'], task_id)
        if result == 'success':
            return {
                'status': 'success',
                'message': 'Task marked as done successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Something went wrong'
            }
    else:
        return redirect(url_for('auth.login'))

#edit task
@blueprint.route('/edit_task/<taskid>', methods=['GET'])
def edit_task(taskid):
    if 'auth_token' in session:
        user = session.get('username')
        user = model.get_user(user)
        task = model.get_task(user['username'], taskid)
        return render_template('pages/addtask/edit.html', user=user, task=task)
    else:
        return redirect(url_for('auth.login'))

#update task
@blueprint.route('/update_task', methods=['UPDATE'])
def update_task():
    if 'auth_token' in session:
        user = session.get('username')
        user = model.get_user(user)
        task  = {
            'id': request.form['id'],
            'task': request.form['task'],
            'description': request.form['description'],
            'priority': request.form['priority']
        }
        result = model.update_task(user['username'], task)
        if result == 'success':
            return {
                'status': 'success',
                'message': 'Task updated successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Something went wrong'
            }
    else:
        return redirect(url_for('auth.login'))