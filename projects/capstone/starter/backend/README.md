## Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.Authorised users will be able to create, view, update, delete movies and actors details.

## Backend URL : https://manivarma-capstone.herokuapp.com/

## Installing Dependencies for the Backend
Python 3.7.9 - Follow instructions to install the latest version of python for your platform in the python docs

Virtual Enviornment - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

PIP Dependencies - Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

pip install -r requirements.txt which will install all of the required packages we selected within the requirements.txt file.

## Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

## Database setup

The `models.py` file contains connection instructions to the Postgres database, which must also be setup and running. Provide a valid username and password, if applicable. 

1. Create a database with name `castingagency` using Psql CLI:

```
create database castingagency;
```

2. Initiate and migrate the database with the following commands in command line:

```
flask db init
flask db migrate
flask db upgrade
```

This will create all necessary tables and relationships to work with the project.

## Running the local development server

All necessary credential to run the project are provided in the `setup.sh` file. The credentials can be enabled by running the following command:  source setup.sh

To run the API server on a local development environmental the following commands must be additionally executed:

### On Linux: export
export FLASK_APP=app.py
export FLASK_ENV=development
 
### On Windows: set
set FLASK_APP=app.py
set FLASK_ENV=development

## Running the server
To run the server, execute: FLASK run or python app.py

API Endpoints
GET '/movies'

## RBAC credentials and roles

Auth0 was set up to manage role-based access control for two users. The API documentation below describes, among others, by which user the endpoints can be accessed. Access credentials and permissions are handled with JWT tockens which must be included in the request header. 

### Permissions
get:movies	       - read server to fetch movies	
get:movies-details - detail	read server to fetch details of the movie	
post:movies	       - add movies to the server	
patch:movies	     - update movies to the server	
delete:movies	     - remove movies from the server	
get:actors	       - read server to fetch actors	
get:actors-detail	-- read server to fetch details of the actors	
post:actors	      -- add actors to the server	
patch:actors	    -- update actors to the server	
delete:actors	    --  remove actors from the server

### Returns all the movies, actors
Roles authorized : Assistant, Director, Producer.

1) Assistant Role user logon details
    login id: manivarma_tv@hotmail.com 
    password: Coffee@123

2) Director Role user logon details
     login id: manivarma@gmail.com    
    password : Coffee@123

3) Producer Role user logon details
    login id : letmein@dummy.com
    password : A@12345678

### Generate JWT Token using
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}


YOUR DOMAIN      : manifsnd.us.auth0.com 
API_IDENTIFIER   : castingagency
YOUR_CLIENT_ID   : 26G1Rz6jMZoFVcoAFwRAuKXPlN49sthL
YOUR_CALLBACK_URI: http://localhost:8100/


### API endpoints and Sample response:

{
    "movies": [
        {
            "id": 3,
            "release_date": "Mon, 07 Feb 2022 00:00:00 GMT",
            "title": "The Life is so Beautiful"
        }
    ],
    "success": true
}
GET /movies/int:id

Fetches movies based on the specific id provided
Request Arguments: page:int
Roles authorized : Assistant,Director, Producer.
sample response:

{
 "movie": {
        "id": 4,
        "release_date": "Wed, 01 Feb 2023 00:00:00 GMT",
        "title": "Kill Bill"
    },
    "success": true
}
POST /movies

Creates a new movie based on a payload.
Request Body: {'title': 'The Little Boy','release_date': '28/04/2022'} (all fields are mandatory)
Roles authorized : Producer.
sample response:

{
 "movie": {
    "id": 3,
    "release_date": "Wed, 27 Apr 2022 18:30:00 GMT",
    "title": "The Little Boy"
  },
  "success": true
}
PATCH /movies/int:id

Updates a movies based on payload.
Roles authorized : Director, Producer.
sample response:

{
 "movie": {
    "id": 3,
    "release_date": "Wed, 27 Apr 2022 18:30:00 GMT",
    "title": "Little Boy"
  },
  "success": true
}
DELETE /movies/int:id

Deletes a movie based on url query parameter
Roles authorised: Producer.
sample response:

{
 "message": "movie id 6, titled The Ghost Rider",
 "success": true
}
GET /actors

Returns all the actors
Roles authorized : Casting Assistant,Casting Director,Executive Producer.
sample response:

{
"actors": [
    {
      "age": 30,
      "gender": "male",
      "id": 1,
      "name": "Will Smith"
    },
    {
      "age": 40,
      "gender": "male",
      "id": 2,
      "name": "Jim Carry"
    }
  ],
  "success": true
  }
GET /actors/int:id

Fetches actor based on the id provided
Roles authorized : Casting Assistant,Casting Director,Executive Producer.
sample response:

{
  "actor": {
    "age": 30,
    "gender": "male",
    "id": 1,
    "name": "Will Smith"
  },
  "success": true
}
POST /actors

Creates new actor based on the payload provided
Roles authorized : Casting Director,Executive Producer.
sample response:

{
  "actor": {
    "age": 22,
    "gender": "female",
    "id": 3,
    "name": "Jennifer"
  },
  "success": true
}
PATCH /actors/int:id

Updates an actor details based on the payload provided
Roles authorized : Casting Director,Executive Producer.
sample response:

{
  "actor": {
    "age": 32,
    "gender": "female",
    "id": 3,
    "name": "Diana"
  },
  "success": true
}
DELETE /actors/int:id

Deletes an actor based on id provided in url query parameter
Roles authorized : Casting Director,Executive Producer.
sample response:

{
  "message": "actor id 3, named Diana is deleted",
  "success": true
}
Error Responses
400 – bad request 401 – unauthorized 404 – resource not found 422 – unprocessable 500 – internal server error

Sample error response

{
 "error": 422,
 "success": false
 "message": "Not processable"
}
Sample RBAC error response

{
  "code": "unauthorized",
  "description": "Permission not found."
}

### Testing
The testing of all endpoints was implemented with unittest. Each endpoint can be tested with one success test case and one error test case. RBAC feature can also be tested for company user and candidate user.

All test cases are in test_app.py file.

To run the tests,

Replace the jwt tokens if required in test_app.py with the ones generated on the website.

For testing locally, we need to reset database. To reset database, run

python manage.py db downgrade
python manage.py db upgrade

py test_app.py