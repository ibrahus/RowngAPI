# RowngAPI

### Installing Dependencies for the project

1. **Python** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, run:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL.
- If run locally, the app is hosted at the default, `http://127.0.0.1:5000/`
- Authentication: The app use AUTH0 authentication

The API will return those error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 401: Unauthorized error
- 403: Forbidden
- 500: Internal Server Erro

### Endpoints 
#### GET /vendors
- Returns a list of vendors objects and success value.
- Require (GET:vendors) permission

#### GET /user-bookings/${user_id}
- Returns a list of booking object for that user
- Require (GET:user-booking) permission

#### GET /vendor-bookings/${vendor_id}
- Returns a list of booking object for that vendor
- Require (GET:vendor-booking) permission

#### POST /create-vendor/
- Send a post request in order to create new vendor
- request body:
{
    "name": "Vendor 2 name",
    "city": "Riyadh",
    "address": "Vendor 2 address",
    "start_duty_time": 9,
    "end_duty_time": 9
}
- Require (POST:create-vendor) permission

#### POST /create-user/
- Send a post request in order to create new user
- request body:
{
    "name": "User 2 name",
    "city": "User 2 city"
}
- Require (POST:create-user) permission


#### POST /create-service/
- Send a post request in order to create new service
- request body:
{
    "vendor_id": 1,
    "service_name": "Service 2 name",
    "service_price": 2,
    "service_duration": 1
}
- Require (POST:create-service) permission


#### POST /create-booking/
- Send a post request in order to create new booking
- request body:
{
    "vendor_id": 1,
    "user_id": 1,
    "services": [1,2],
    "booking_date": "2021-08-04 09:00:00"
}
- Require (POST:create-booking) permission


		POST: add new booking
		PATCH: update a booking <int: booking id>
    DELETE: delete a booking <int: booking id>
