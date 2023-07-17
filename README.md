# Jagaad Stats API

The Jagaad Stats API is a REST API that collects and provides statistical information about processed messages in a system. It allows tracking the number of messages and the total amount processed for each customer ID and message type within a specified date interval.

## Table of Contents

- [Jagaad Stats API](#jagaad-stats-api)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Technologies Used](#technologies-used)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Testing](#testing)
  - [License](#license)

## Requirements

To run the Jagaad Stats API, you need the following:

- Docker and Docker Compose

## Technologies Used

The Jagaad Stats API is built using the following technologies:

- Python: The programming language used to develop the API.
- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- PostgreSQL: A popular open-source relational database.
- Docker: A containerization platform for packaging the application and its dependencies.

## Usage

To start the Jagaad Stats API, use the following command:

1.  Build the docker image

```bash
$ docker build -t jagaadapi .
```

2. Run the app with docker-compose

```bash
$ docker-compose up -d
```

The API will be accessible at http://0.0.0.0:80.

## API Endpoints

**Swagger UI (API documentation)**: Visit http://0.0.0.0:80/docs to interact with the API using the Swagger UI. It provides a user-friendly interface to explore and test the available endpoints.

OR

**ReDoc (API documentation)**: Alternatively, you can access the API documentation using the ReDoc UI at http://0.0.0.0:80/redoc. ReDoc provides a clean and simple interface to view and understand the API specification.

## Testing

To run the tests for the Jagaad Stats API, use the following command:

1. (Optionnal) Set up a virtual environment

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Install all the required dependencies

```bash
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

3. Run the tests

```bash
$ pytest
```

The tests will be executed, and the results will be displayed in the console.


## License

This project is licensed under the [MIT License](LICENSE).

---
