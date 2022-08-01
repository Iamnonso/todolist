import os
from sqlite3 import Cursor
from flask import session
from ..myhelper import myhelper

class MySqlDb:
    '''this function will execute the query and return the result'''
    def __init__(self, mysql):
        self.query = mysql
        self.db = os.environ.get('DB')
        self.user = os.environ.get('USER')
        self.password = os.environ.get('PASSWORD')
        self.host = os.environ.get('HOST')
    
    def login(self, username, password):
        cursor = self.query.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, username))
        result = cursor.fetchone()
        cursor.close()
        if result:
            if result['username'] == username or result['email'] == username:
                is_password_correct = myhelper.checkpassword(password, result['password'])
                if is_password_correct:
                    session['auth_token'] = myhelper.get_uuid_id()
                    session['username'] = result['username']
                    session['user'] = result
                    return 'success'
                else:
                    return 'password incorrect'
            else:
                return False
        else:
            return False
    def create_account(self, fullname, username, email, password):
        cursor = self.query.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return 'account exists'
        else:
            cursor = self.query.connection.cursor()
            cursor.execute("INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)", (fullname, username, email, password))
            self.query.connection.commit()
            cursor.close()
            return 'success'
    def get_user(self, username):
        cursor = self.query.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result
        else:
            return False
    def delete_user(self, id):
        cursor = self.query.connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", [id])
        self.query.connection.commit()
        #delete all tasks
        if cursor.rowcount > 0:
            cursor.execute("DELETE FROM task WHERE userid = %s", [id])
            self.query.connection.commit()
            cursor.close()
            return 'success'

    def check_email(self, email):
        cursor = self.query.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", [email])
        result = cursor.fetchone()
        cursor.close()
        if result:
            return True
        else:
            return False
    def edit_user(self, id, fullname, username, email):
        cursor = self.query.connection.cursor()
        #check if username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        result = cursor.fetchone()
        cursor.close()
        if result:
            if result['id'] == id:
                cursor = self.query.connection.cursor()
                cursor.execute("UPDATE users SET name = %s, username = %s, email = %s WHERE id = %s", (fullname, username, email, id))
                self.query.connection.commit()
                cursor.close()
                return 'success'
            else:
                return 'account exists'
    def get_tasks(self, username):
        cursor = self.query.connection.cursor()
        #GET ALL TASKS ORDER BY ID
        cursor.execute("SELECT * FROM task WHERE userid = %s ORDER BY id DESC", [username])
        result = cursor.fetchall()
        cursor.close()
        if result:
            return result
        else:
            return False
    def add_task(self, userid, task):
        cursor = self.query.connection.cursor()
        task_date = myhelper.get_time()
        try:
            cursor.execute("INSERT INTO task (userid, taskheading, description, category, priority, status, date) VALUES (%s, %s, %s, %s, %s, %s, %s)", (userid, task['task'], task['description'], task['Category'], task['priority'], 'active',  task_date))
            self.query.connection.commit()
            cursor.close()
            return 'success'
        except Exception as e:
            return e
    def delete_task(self,userid, id):
        cursor = self.query.connection.cursor()
        try:
            cursor.execute("DELETE FROM task WHERE id = %s AND userid = %s", [id, userid])
            self.query.connection.commit()
            cursor.close()
            return 'success'
        except Exception as e:
            return e
    def mark_task(self, userid, id):
        cursor = self.query.connection.cursor()
        try:
            cursor.execute("UPDATE task SET status = 'completed' WHERE id = %s AND userid = %s", [id, userid])
            self.query.connection.commit()
            cursor.close()
            return 'success'
        except Exception as e:
            return e
    def get_task(self, userid, id):
        cursor = self.query.connection.cursor()
        try:
            cursor.execute("SELECT * FROM task WHERE id = %s AND userid = %s", [id, userid])
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result
            else:
                return False
        except Exception as e:
            return e
    def update_task(self, userid, task):
        cursor = self.query.connection.cursor()
        try:
            cursor.execute("UPDATE task SET taskheading = %s, description = %s, priority = %s WHERE id = %s AND userid = %s", (task['task'], task['description'], task['priority'], int(task['id']), userid))
            self.query.connection.commit()
            cursor.close()
            return 'success'
        except Exception as e:
            return e