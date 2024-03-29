# Automated Testing Demo Project
Project that can showcase my proficiency in Python development, automated testing, Docker and continuous integration. 

It implements:
- backend server with Fast API
- dockerizing  Fast API server app
- simple set of API CRUD tests plus some extras
- GitHub Actions integration (CI - building server and running tests)

### Server

Run server from terminal:
> uvicorn main:app --host 0.0.0.0 --port 8000 --reload

API documentation:
- Swagger UI: 
    > http://127.0.0.1:8000/docs
- ReDoc:
    > http://127.0.0.1:8000/redoc

To build API server image and run container:
> docker build -t posts-api .
> docker run -d -p 8000:80 posts-api

To build API server while developing API:
> docker-compose up --build

To start API server:
> docker-compose up

To stop API server:
> docker-compose down

### Tests

Assuming you have Python 3.11 installed:

To run tests in terminal:
> python -m pytest -vv -s

you can also add the `--log-cli-level=INFO (DEBUG)` parameter to print logs to console

### Continuous Integration

Check GH [Actions](https://github.com/olga-khomenko/automated-testing-demo/actions) tab to see CI jobs.
