from flask import Flask, render_template, redirect, session, request
import random

from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe"

#crud

#read
@app.route("/")
def index():
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users"
    users = mysql.query_db(query)
    print(users)
    return render_template("user.html")


@app.route("/user/<int:user_id>")
def display_user(user_id):
    print(user_id)
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users WHERE id = %(id)s;"
    
    data = {
        "id": user_id
    }
    user_from_database = mysql.query_db(query, data)
    print(user_from_database)
    return render_template("index.html", user = user_from_database[0])

@app.route("/users")
def display_users():
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users;"

    users_from_database = mysql.query_db(query)
    print('returning all users from db: ', users_from_database)
    return render_template("user.html", users = users_from_database)

@app.route("/users/new")
def add_user():
    return render_template("new_user.html")

#create

@app.route("/users/new/create", methods = ["POST"])
def createUser():
    mysql = connectToMySQL("users_schema")
    insert_query = "INSERT INTO users(first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, now(), now());"

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    row_id = mysql.query_db(insert_query, data)
    return redirect("/users")


#update
@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        "id": user_id
    }
    user_from_database = mysql.query_db(query, data)

    return render_template("edit_user.html", user = user_from_database[0])


@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    mysql = connectToMySQL("users_schema")
    insert_query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "id": user_id
    }
    
    mysql.query_db(insert_query, data)
    return redirect("/users")


#delete
@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    mysql = connectToMySQL("users_schema")
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        "id": user_id
    }
    mysql.query_db(query, data) 

    return redirect("/users")

@app.route('/user/<int:user_id>/delete')
def delete_user2(user_id):
    mysql = connectToMySQL("users_schema")
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        "id": user_id
    }
    mysql.query_db(query, data) 

    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)