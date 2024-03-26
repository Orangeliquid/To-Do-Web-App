from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bootstrap import Bootstrap5
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import os
from bson import ObjectId

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
bootstrap = Bootstrap5(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['todo_app']
users_collection = db['users']
todos_collection = db['todos']
finished_collection = db['finished_todos']


# Define Todo model
class Todo:
    def __init__(self, category, description, due_date, user_id):
        self.category = category
        self.description = description
        self.due_date = due_date
        self.user_id = user_id


# Index app route creation
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'sign-in' in request.form:
            email = request.form['email']
            password = request.form['password']
            user = users_collection.find_one({'email': email})

            if user and check_password_hash(user['password'], password):
                # Convert ObjectId to string before storing in session
                user['_id'] = str(user['_id'])
                session['user'] = user
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid email or password. Please try again.", "error")

    return render_template("index.html")


@app.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['passwordConfirm']

        # Check if passwords match
        if password != password_confirm:
            print("Password does not match")
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for('signup'))

        # Check if user already exists
        if users_collection.find_one({'email': email}):
            print(f"Email already exists: {email}")
            flash("Email already exists. Please choose a different email.", "error")
            return redirect(url_for('signup', _anchor='sign-up'))

            # Hash password before storing
        hashed_password = generate_password_hash(password)

        # Insert user into MongoDB
        users_collection.insert_one({'email': email, 'password': hashed_password})

        # Redirect to home page after sign-up
        flash("Sign-up successful. Please sign in.", "success")
        return redirect(url_for('home'))

    return render_template("signup.html")


@app.route("/sign-out")
def signout():
    if 'user' in session:
        session.pop('user', None)
        flash("You have been successfully signed out.", "success")
        return redirect(url_for('home'))
    else:
        flash("You are not signed in.", "error")
        return redirect(url_for('home'))


@app.route("/dashboard")
def dashboard():
    if 'user' in session:
        user_id = session['user']['_id']
        user_todos = todos_collection.find({'user_id': user_id})
        return render_template("dashboard.html", todos=user_todos)
    else:
        # User is not signed in, redirect to the sign-in page
        flash("You must be signed in to access the dashboard.", "error")
        return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template("about.html")


# Route for adding a todo
@app.route("/add-todo", methods=['POST'])
def add_todo():
    if 'user' in session:
        # Get todo data from the request
        todo_data = request.json
        category = todo_data['category']
        description = todo_data['description']
        due_date = todo_data['due_date']
        user_id = session['user']['_id']

        # Create a new Todo instance
        new_todo = Todo(category, description, due_date, user_id)

        # Insert the new todo into the database
        todos_collection.insert_one(new_todo.__dict__)

        # Return success response
        return jsonify({'success': True})
    else:
        # Return error response
        return jsonify({'success': False, 'message': 'User not logged in'})


@app.route("/delete-todo/<todo_id>", methods=['POST'])
def delete_todo(todo_id):
    if 'user' in session:
        user_id = session['user']['_id']
        todos_collection.delete_one({'_id': ObjectId(todo_id), 'user_id': user_id})
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "User not authenticated"}), 401


@app.route("/mark-finished/<todo_id>", methods=['POST'])
def mark_finished(todo_id):
    if 'user' in session:
        user_id = session['user']['_id']
        todo = todos_collection.find_one({'_id': ObjectId(todo_id), 'user_id': user_id})
        if todo:
            # Move the todo to the finished collection
            finished_collection.insert_one(todo)
            # Remove the todo from the todos collection
            todos_collection.delete_one({'_id': ObjectId(todo_id), 'user_id': user_id})
            return jsonify({"message": "Todo item marked as finished successfully"})
        else:
            return jsonify({"error": "Todo item not found or unauthorized access"}), 404
    else:
        return jsonify({"error": "User not authenticated"}), 401


@app.route("/get-finished-todos")
def get_finished_todos():
    if 'user' in session:
        user_id = session['user']['_id']
        finished_todos = finished_collection.find({'user_id': user_id})
        # Convert ObjectId to string for JSON serialization
        finished_todos = [{'_id': str(todo['_id']), 'category': todo['category'], 'description': todo['description'],
                           'due_date': todo['due_date']} for todo in finished_todos]
        return jsonify(finished_todos)
    else:
        return jsonify({'error': 'User not authenticated'}), 401


@app.route("/delete-finished-todo/<todo_id>", methods=['POST'])
def delete_finished_todo(todo_id):
    if 'user' in session:
        user_id = session['user']['_id']
        finished_collection.delete_one({'_id': ObjectId(todo_id), 'user_id': user_id})
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "User not authenticated"}), 401


if __name__ == "__main__":
    app.run(debug=True, port=5002)