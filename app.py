import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Create a Flask application
app = Flask(__name__)

# Configure the Flask application with necessary DB/JWT settings
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = bool(
    os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)

# Initialize Flask JWT Manager
jwt = JWTManager(app)

# Initialize Flask SQLAlchemy
db = SQLAlchemy(app)

# Import data models
from models import Blog, User

# Ensure that we are in the application context before creating the database tables
with app.app_context():
    # Create all database tables based on the defined models
    db.create_all()


# Define a route for testing purposes
@app.route("/api/test", methods=["GET"])
def test_route():
    """
    A test route to check if the API is working fine.

    Returns:
        jsonify: A JSON response with a success message.
    """
    return jsonify({"message": "API is working fine"})


# Route for user registration
@app.route("/api/register", methods=["POST"])
def register_user():
    """
    Endpoint for user registration.

    Returns:
        jsonify: A JSON response indicating the success or failure of the registration.
    """
    # Get JSON data from the request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Check if both username and password are provided
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    # Generate password hash
    password_hash = generate_password_hash(password)

    # Create a new user and add it to the database
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# Route for user login
@app.route("/api/login", methods=["POST"])
def login_user():
    """
    Endpoint for user login.

    Returns:
        jsonify: A JSON response indicating the success or failure of the login attempt.
    """
    # Get JSON data from the request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password_hash, password):
        response = jsonify({"msg": "Login successful"})
        access_token = create_access_token(identity=username)
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


# Route for user logout with cookies
@app.route("/api/logout", methods=["POST"])
def logout():
    """
    Endpoint for user logout with cookies.

    Returns:
        jsonify: A JSON response indicating the success of the logout.
    """
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response


# Route for retrieving all blogs
@app.route("/api/blogs", methods=["GET"])
@jwt_required()
def get_blogs():
    """
    Endpoint for retrieving all blogs.

    Returns:
        dict: A dictionary containing blog data.
    """
    # Query all blogs from the database
    blogs = Blog.query.all()

    # Format the response data
    res = [{"title": obj.title, "content": obj.content} for obj in blogs]

    return {"data": res}


# Route for retrieving a specific blog by ID
@app.route("/api/blogs/<int:blog_id>", methods=["GET"])
@jwt_required()
def get_specific_blog(blog_id):
    """
    Endpoint for retrieving a specific blog by ID.

    Args:
        blog_id (int): The ID of the blog.

    Returns:
        jsonify: A JSON response containing the blog details or a not found message.
    """
    # Query the database for the specific blog by ID
    blog = Blog.query.get(blog_id)

    if blog:
        # Return blog details if the blog exists
        return jsonify({"id": blog.id, "title": blog.title, "content": blog.content})
    else:
        # Return a not found message if the blog does not exist
        return jsonify({"message": "Blog not found"}), 404


# Route for creating a new blog
@app.route("/api/blogs", methods=["POST"])
@jwt_required()
def create_blog():
    """
    Endpoint for creating a new blog.

    Returns:
        jsonify: A JSON response indicating the success of the blog creation and the blog ID.
    """
    # Get JSON data from the request
    data = request.get_json()

    # Get the current user's identity
    current_user = get_jwt_identity()

    # Query the user object from the database based on the current user's username
    user_obj = User.query.filter_by(username=current_user).first()

    # Create a new blog object with the provided data
    new_blog = Blog(
        title=data["title"],
        content=data["content"],
        author=current_user,
        user_id=user_obj.id,
    )

    # Add the new blog to the database and commit the changes
    db.session.add(new_blog)
    db.session.commit()

    # Return a JSON response indicating the success of the blog creation and the blog ID
    return jsonify({"message": "Blog created successfully", "id": new_blog.id}), 201


# Route for updating an existing blog
@app.route("/api/blogs/<int:blog_id>", methods=["PUT"])
@jwt_required()
def update_blog(blog_id):
    """
    Endpoint for updating an existing blog.

    Args:
        blog_id (int): The ID of the blog to be updated.

    Returns:
        jsonify: A JSON response indicating the success or failure of the blog update.
    """
    # Get the current user's identity
    current_user = get_jwt_identity()

    # Query the user object from the database based on the current user's username
    user_obj = User.query.filter_by(username=current_user).first()

    # Get the current user's ID
    current_user_id = user_obj.id

    # Query the blog from the database based on the provided blog ID
    blog = Blog.query.get(blog_id)

    if blog:
        # Get the user ID associated with the blog
        blog_user_id = blog.user_id

        if current_user_id == blog_user_id:
            # If the current user is the author of the blog, update the blog content
            data = request.get_json()
            blog.title = data["title"]
            blog.content = data["content"]
            db.session.commit()
            return jsonify({"message": "Blog updated successfully"})
        else:
            # If the current user is not the author, return an unauthorized response
            return (
                jsonify(
                    {"message": f"User {current_user} unauthorized to update this blog"}
                ),
                403,
            )
    else:
        # If the blog is not found, return a not found response
        return jsonify({"message": "Blog not found"}), 404


# Route for deleting an existing blog
@app.route("/api/blogs/<int:blog_id>", methods=["DELETE"])
@jwt_required()
def delete_blog(blog_id):
    """
    Endpoint for deleting an existing blog.

    Args:
        blog_id (int): The ID of the blog to be deleted.

    Returns:
        jsonify: A JSON response indicating the success or failure of the blog deletion.
    """
    # Get the current user's identity
    current_user = get_jwt_identity()

    # Query the user object from the database based on the current user's username
    user_obj = User.query.filter_by(username=current_user).first()

    # Get the current user's ID
    current_user_id = user_obj.id

    # Query the blog from the database based on the provided blog ID
    blog = Blog.query.get(blog_id)

    if blog:
        # Get the user ID associated with the blog
        blog_user_id = blog.user_id

        if current_user_id == blog_user_id:
            # If the current user is the author of the blog, delete the blog
            db.session.delete(blog)
            db.session.commit()
            return jsonify({"message": "Blog deleted successfully"})
        else:
            # If the current user is not the author, return an unauthorized response
            return (
                jsonify(
                    {"message": f"User {current_user} unauthorized to delete this blog"}
                ),
                403,
            )
    else:
        # If the blog is not found, return a not found response
        return jsonify({"message": "Blog not found"}), 404
