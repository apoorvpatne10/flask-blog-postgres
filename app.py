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


with app.app_context():
    db.create_all()


@app.route("/api/test", methods=["GET"])
def test_route():
    return jsonify({"message": "api working fine"})


@app.route("/api/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    password_hash = generate_password_hash(password)

    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity=username)
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route("/api/logout", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route("/api/blogs", methods=["GET"])
@jwt_required()
def get_blogs():
    blogs = Blog.query.all()
    res = [{"title": obj.title, "content": obj.content} for obj in blogs]
    return {"data": res}


@app.route("/api/blogs/<int:blog_id>", methods=["GET"])
@jwt_required()
def get_specific_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog:
        return jsonify({"id": blog.id, "title": blog.title, "content": blog.content})
    else:
        return jsonify({"message": "Blog not found"}), 404


@app.route("/api/blogs", methods=["POST"])
@jwt_required()
def create_blog():
    data = request.get_json()
    current_user = get_jwt_identity()
    user_obj = User.query.filter_by(username=current_user).first()

    new_blog = Blog(
        title=data["title"],
        content=data["content"],
        author=current_user,
        user_id=user_obj.id,
    )
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({"message": "Blog created successfully", "id": new_blog.id}), 201


@app.route("/api/blogs/<int:blog_id>", methods=["PUT"])
@jwt_required()
def update_blog(blog_id):
    current_user = get_jwt_identity()
    user_obj = User.query.filter_by(username=current_user).first()
    current_user_id = user_obj.id
    blog = Blog.query.get(blog_id)

    if blog:
        blog_user_id = blog.user_id

        if current_user_id == blog_user_id:
            data = request.get_json()
            blog.title = data["title"]
            blog.content = data["content"]
            db.session.commit()
            return jsonify({"message": "Blog updated successfully"})
        else:
            return (
                jsonify(
                    {"message": f"User {current_user} unauthorized to update this blog"}
                ),
                403,
            )
    else:
        return jsonify({"message": "Blog not found"}), 404


@app.route("/api/blogs/<int:blog_id>", methods=["DELETE"])
@jwt_required()
def delete_blog(blog_id):
    current_user = get_jwt_identity()
    user_obj = User.query.filter_by(username=current_user).first()
    current_user_id = user_obj.id
    blog = Blog.query.get(blog_id)

    if blog:
        blog_user_id = blog.user_id

        if current_user_id == blog_user_id:
            db.session.delete(blog)
            db.session.commit()
            return jsonify({"message": "Blog deleted successfully"})
        else:
            return (
                jsonify(
                    {"message": f"User {current_user} unauthorized to delete this blog"}
                ),
                403,
            )
    else:
        return jsonify({"message": "Blog not found"}), 404
