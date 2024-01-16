# flask-blog-postgres

This is a simple Flask-based API for managing a blog system. The API includes functionality for user registration, login, logout, and CRUD operations (Create, Read, Update, Delete) on blog entries. It utilizes Flask-SQLAlchemy for database interaction and Flask-JWT-Extended for handling JSON Web Tokens.

## Getting Started

### Prerequisites

Before you begin, ensure you have Python and Flask installed. Additionally, you'll need to set up a PostgreSQL database and provide the necessary environment variables. The required environment variables are defined in the `.env` file.

### Installation

1. Clone the repository:

```
git clone https://github.com/apoorvpatne10/flask-blog-postgres
```

2. Change into the project directory:

```
cd flask-blog-postgres
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the root of the project and set the following variables:

```
DATABASE_URL=your_postgresql_database_url
SQLALCHEMY_TRACK_MODIFICATIONS=False
JWT_SECRET_KEY=your_jwt_secret_key
```

2. Replace `your_postgresql_database_url` with the connection URL for your PostgreSQL database, and set a secure value for `your_jwt_secret_key`.

### Running the Application

1. Run the Flask application:

```
flask run
```

2. The API will be accessible at `http://localhost:5000/`. Send a sample get request to `http://localhost:5000/api/test` to test if the API is working fine.

### API Endpoints

#### Test Route

- **URL**: `/api/test`
- **Method**: `GET`
- **Description**: A test route to check if the API is working fine.
- **Response**: JSON response with a success message.

#### User Registration

- **URL**: `/api/register`
- **Method**: `POST`
- **Description**: Endpoint for user registration.
- **Request Body**:

```
{
  "username": "your_username",
  "password": "your_password"
}
```

- **Response**: JSON response indicating the success or failure of the registration.

#### User Login

- **URL**: `/api/login`
- **Method**: `POST`
- **Description**: Endpoint for user login.
- **Request Body**:

```
{
  "username": "your_username",
  "password": "your_password"
}
```

- **Response**: JSON response indicating the success or failure of the login attempt. Includes an access token in case of successful login.

#### User Logout

- **URL**: `/api/logout`
- **Method**: `POST`
- **Description**: Endpoint for user logout.
- **Response**: JSON response indicating the success of the logout.

#### Get All Blogs

- **URL**: `/api/blogs`
- **Method**: `GET`
- **Description**: Endpoint for retrieving all blogs.
- **Authorization**: Requires a valid JWT token.
- **Response**: JSON response containing a list of blogs.

#### Get Specific Blog by ID

- **URL**: `/api/blogs/<int:blog_id>`
- **Method**: `GET`
- **Description**: Endpoint for retrieving a specific blog by ID.
- **Authorization**: Requires a valid JWT token.
- **Response**: JSON response containing the blog details or a not found message.

#### Create New Blog

- **URL**: `/api/blogs`
- **Method**: `POST`
- **Description**: Endpoint for creating a new blog.
- **Authorization**: Requires a valid JWT token.
- **Request Body**:

```
{
  "title": "Blog Title",
  "content": "Blog Content"
}
```

- **Response**: JSON response indicating the success of the blog creation and the blog ID.

#### Update Existing Blog

- **URL**: `/api/blogs/<int:blog_id>`
- **Method**: `PUT`
- **Description**: Endpoint for updating an existing blog.
- **Authorization**: Requires a valid JWT token.
- **Request Body**:

```
{
  "title": "Updated Blog Title",
  "content": "Updated Blog Content"
}
```

- **Response**: JSON response indicating the success or failure of the blog update.

#### Delete Existing Blog

- **URL**: `/api/blogs/<int:blog_id>`
- **Method**: `DELETE`
- **Description**: Endpoint for deleting an existing blog.
- **Authorization**: Requires a valid JWT token.
- **Response**: JSON response indicating the success or failure of the blog deletion.
