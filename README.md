# RowngAPI
Rowng is an intermediary application between the cosmetic service provider and the client.
This project is to build the API for the app.

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

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

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
- Base URL: https://fsnd-rowng-api.herokuapp.com/
- If run locally, the app is hosted at the default, `http://127.0.0.1:5000/`
- Authentication: The app use AUTH0 authentication. Two roles are created, each role has a set of permissions described as folow:
    - Vendor:
        - GET:vendor-booking
        - POST:create-vendor
        - POST:create-service
        - PATCH:update-booking
    - User:
        - GET:vendors
        - GET:user-booking
        - POST:create-user
        - POST:create-booking
        - PATCH:update-booking
        - DELETE:delete-booking

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
- Example response:
```
{
    "success": true,
    "vendors": [
        {
            "address": "Vendor 1 address",
            "city": "Riyadh",
            "end_duty_time": "09:00:00",
            "id": 1,
            "name": "Vendor 1 name",
            "start_duty_time": "09:00:00"
        }
    ]
}
```

#### GET /user-bookings/${user_id}
- Returns a list of booking object for that user
- Require (GET:user-booking) permission
- Example response:
```
{
    "success": true,
    "user_bookings": [
        {
            "booking_date": "Thu, 05 Aug 2021 14:20:16 GMT",
            "booking_id": 1,
            "services": [
                {
                    "service_duration": "01:00:00",
                    "service_name": "Service 1 name",
                    "service_price": 100
                }
            ],
            "user_name": "User 1 name",
            "vendor_name": "Vendor 1 name"
        }
    ]
}
```

#### GET /vendor-bookings/${vendor_id}
- Returns a list of booking object for that vendor
- Require (GET:vendor-booking) permission
- Example response:
```
{
    "success": true,
    "vendor_bookings": [
        {
            "booking_date": "Thu, 05 Aug 2021 14:20:16 GMT",
            "booking_id": 1,
            "services": [
                {
                    "service_duration": "01:00:00",
                    "service_name": "Service 1 name",
                    "service_price": 100
                }
            ],
            "user_name": "User 1 name",
            "vendor_name": "Vendor 1 name"
        }
    ]
}
```

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
- Example response:
```
{
{
    "success": true,
    "vendor": {
        "address": "Vendor 2 address",
        "city": "Riyadh",
        "end_duty_time": "09:00:00",
        "id": 2,
        "name": "Vendor 2 name",
        "start_duty_time": "09:00:00"
    }
}
```

#### POST /create-user/
- Send a post request in order to create new user
- request body:
{
    "name": "User 2 name",
    "city": "User 2 city"
}
- Require (POST:create-user) permission
- Example response:
```
{
    "success": true,
    "user": {
        "city": "User 2 city",
        "id": 2,
        "name": "User 2 name"
    }
}
```

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
- Example response:
```
{
    "service": {
        "id": 2,
        "service_duration": "01:00:00",
        "service_name": "Service 2 name",
        "service_price": 2
    },
    "success": true
}
```

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
- Example response:
```
{
    "booking": {
        "booking_date": "Wed, 04 Aug 2021 09:00:00 GMT",
        "id": 3,
        "services": [
            1,
            2
        ],
        "user_id": 1,
        "vendor_id": 1
    },
    "success": true
}
```

#### PATCH /update-booking/${booking_id}
- Send a post request in order to update a booking
- request body:
{
    "services": [1],
    "booking_date": "2021-08-18 09:00:00"
}
- Require (PATCH:update-booking) permission
- Example response:
```
{
    "booking": {
        "booking_date": "Wed, 18 Aug 2021 09:00:00 GMT",
        "id": 1,
        "services": [
            1
        ],
        "user_id": 1,
        "vendor_id": 1
    },
    "success": true
}
```

#### DELETE /delete-booking/${booking_id}
- Send a post request in order to delete a booking
- Require (DELETE:delete-booking) permission
- Example response:
```
{
    "deleted": 1,
    "success": true
}
```

## Testing
The endpoints are tested with [Postman](https://getpostman.com).
- Import the postman collection `Rowng-API.postman_collection.json`
- Run the collection.
