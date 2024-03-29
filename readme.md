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

3. Create a virtual environment so that the dependencies for this project is isolated from the global python dependencies and activate it.

```
python -m venv env

./env/Scripts/activate
```

4. Install the required dependencies:

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

### Database Setup on AWS RDS

The database setup includes the use of PostgreSQL 15.4-R3, a Dev/Test template, a db.t3.small instance type, and other settings tailored for this demo application.

1. Database Creation

- Choose the "Standard Create" method.
- Select the PostgreSQL engine with version 15.4-R3.
- Choose the "Dev/Test" template for configuration.

2. Instance Configuration

- **DB Instance Identifier**: Choose a unique identifier for your database instance.
- **Credentials Settings**: Set a master username and password for authentication.
- **Instance Class**: Select "Burstable classes" and choose the db.t3.small instance type.

3. Storage Configuration

- **Storage Type**: Choose "gp3" for general-purpose SSD storage.
- **Allocated Storage**: Set the storage capacity to 40 GB.
- **Storage Autoscaling**: Ensure that storage autoscaling is turned off.

4. Connectivity Configuration

- **Compute Resource**: Choose "Don’t connect to an EC2 compute resource."
- **Network Type**: Select IPv4 for network configuration.
- **VPC**: Create a new VPC for the database.
- **Public Access**: Enable public access since it will be interacted with from a Flask API App.
- **VPC Security Group (Firewall)**: Create a security group that allows inbound connections from the machine's IP address.

5. Monitoring Configuration

- Performance Insights and Enhanced Monitoring: Turn off both features as they are not needed for the demo application.

6. Additional Configuration

- **Initial Database Name**: Provide a name for the initial database.
- **Automated Backups**: Disable automated backups for simplicity.
- **Encryption**: Disable encryption for simplicity.

7. Create the Database
   After configuring all the settings, proceed to create the database. Ensure that you review the configurations carefully before initiating the creation process.

8. Fetch the endpoint URL, username, password, initial db name and appropriately replace the `DATABASE_URI` field in `.env` based on following format:

```
postgresql://{username}:{password}@{endpoint_url}:5432/{db_name}
```

### Testing the API via Postman

Follow the instructions from [here](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/#import-postman-data). Drag and Drop the json file provided in this repository and test the endpoints. This postman export json consists of custom setup for including `csrf_token` in HTTP Request Header and some environment variables for ease of testing.

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
