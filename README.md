# Python-MongoDB CRUD

This repository contains a full example on how to locally run MongoDB in a Docker container and using FastAPI to setup a CRUD API.

Clone the repository, create a virtual environment and install dependencies. Start Docker containers and run uvicorn server.

Clone the repository:
```
$ git clone https://github.com/ronnyandre/python-mongo-crud
```

Navigate into the directory and create a virtual environment:

```
$ cd python-mongo-crud
$ python -m venv venv
$ . venv/bin/activate
```

Install Python packages:

```
$ pip install -r requirements.txt
```

Start the MongoDB Docker container:

```
$ docker compose up -d
```

Run the Python server:

```
$ uvicorn app.main:app --reload
```

Navigate to http://localhost:8000/api/v1/healthcheck

API swagger documentation can be found on http://localhost:8000/docs