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

    return render_template("index.html")

# incomplete
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

    return render_template("user.html", user = user_from_database)

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


#delete

if __name__ == "__main__":
    app.run(debug=True)