# Entrance exam to EPL API
This is the backend of the project of the application of EPL's entrance exam.
It's built with python by the FastAPI library for the endpoints's development, motor of the MongoDB database integration
and another libraries.



## Getting Started
To get started with this project, you need to install python and MongoDB in your computer and then follow the steps.

If you really don't want to read the [blog post](https://developer.mongodb.com/quickstart/python-quickstart-fastapi/) and want to get up and running,
activate your Python virtualenv, and then run the following from your terminal (edit the `MONGODB_URL` first!):

```bash
# Install the requirements:
pip install -r requirements.txt

# Configure the location of your MongoDB database:
export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"

#Do not forget to create the .env file using the structure of .env.example with changing the values of your environnement variables

# Start the service:
uvicorn app:app --reload
```


(Check out [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) if you need a MongoDB database.)

Now you can load http://localhost:8000/docs in your browser ... but there won't be much to see until you've inserted some data.

To launch tests:

```bash
#Launch tests
pytest

#Lauch asynchrones tests
pytest-async
```

# Folders structure
The following lines will explain the structure of the folders of the projects in order to make it easier to you to conntinue
with your project
### controllers
This directory contains the routes of the endpoints and their corresponding controllers that are the entrance points of the
requests corresponding to these endpoints
### services
This directory contains the services that are the classes that communicates with the database. The services classes contains 
methods to select items, add, update, delete, etc items in the database
### models
This directory contains the models that represent the schema of the data in tables(collections) of the database
### providers
This directory contains the files that contains the utilities such as hashing passwords, create tokens, etc
### dependencies
This directory contains the dependencies(middlewares) of different endpoints such as authentication dependencies, roles dependencies, etc.
### config
This directory contains different configurations of the application such as database configuration, etc.
### tests
This directory contains the tests: unit tests, integration tests, etc.
It's subdivised in many folders corresponding to the types of tests
### .env
This file contains the environment variables
### .env.example
This file hase a same structure with the .env file and will be the model for making your own .env file
### main.py
This file is the entrance point(main file) of the application
### requirements.txt
This file contains the requirements of the project
### .gitignore
This file contains the files that will be ignored when pushing to github

If you have any questions or suggestions, check out the [MongoDB Community Forums](https://developer.mongodb.com/community/forums/)!