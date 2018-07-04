# Ride My Way

Ride-my App is a carpooling application that provides drivers with the ability to create ride offers
and passengers to join available ride offers.

## Motivation

This is driven by the increase in technology, which has proven to be more effective in time saving.
We there fore develop this app to apply tech in the transportation industry with the main purpose of saving m
ore and earning more.

## Build status, and test coverage

Build status of continuous integration i.e. travis, -
Test coverage of code climate and coveralls -

[![Build Status](https://travis-ci.org/reiosantos/ride-api.svg?branch=feature)](https://travis-ci.org/reiosantos/ride-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/7047d11c77cc6fb3d2db/maintainability)](https://codeclimate.com/github/reiosantos/ride-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7047d11c77cc6fb3d2db/test_coverage)](https://codeclimate.com/github/reiosantos/ride-api/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/reiosantos/ride-api/badge.svg?branch=feature)](https://coveralls.io/github/reiosantos/ride-api?branch=feature)

***Features***

 * Users (Driver and passenger) can fetch all ride offers
 * Users can fetch a specific ride offer
 * Driver creates a ride offer
 * Passengers make a request to join a ride.
 * Driver can deletes and update ride offer

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development
and testing purposes.

### Prerequisites
This describes things needed to install the software.

```bash
- git : to update and clone the repository
- python3: The base language used to develop the api
- pip: a python package used to install project requirements
```

### Installing

```bash
Type: "git clone https://github.com/reiosantos/ride-my-way.git" in your terminal.
```
The UI folder houses the user interface. To access the user interface, open the login.html
file inside the UI/templates folder


The api folder contains the system backend services.

- To install the requirements. run:

```bash
pip3 install -r requirements
```

The app can then be run with the following commands.

```bash
cd api

python run.py
```

- Now you can access the system api via URLs:

* To create an account, method[POST]
```http
http://localhost:5000/api/v1/auth/signup/
```

* To login to an account, method[POST]
```http
http://localhost:5000/api/v1/auth/login/
```
* To create an account, method[POST]
```http
http://localhost:5000/api/v1/auth/signup/
```

* To access all rides, method[GET]
```http
http://localhost:5000/apis/v1/rides/
```

* To access a particular ride. ie ride number 5, method[GET]
```http
http://localhost:5000/apis/v1/rides/5/
```

* To delete a particular ride for-example 4, method[DELETE]
```http
http://localhost:5000/apis/v1/rides/4/
```

* To update a particular ride, method[PUT]
```http
http://localhost:5000/api/v1/rides/
```

* To insert a new ride, method[POST]
```http
http://localhost:5000/api/v1/rides/
```

* To send a request to join a particular ride for-example 4, method[POST]
```http
http://localhost:5000/apis/v1/rides/4/request/
```

* To view requests for a particular ride for-example 4, method[GET]
```http
http://localhost:5000/apis/v1/rides/4/request/
```

* To update a request for a ride for-example 4, 
and request number 5 hod[PUT]
```http
http://localhost:5000/apis/v1/rides/4/request/5/
```

* To delete a request of a particular ride 
for-example 4, and ride 5 method[DELETE]
```http
http://localhost:5000/apis/v1/rides/4/request/5/
```

## Running the tests

- To run the tests, make sure you are working under api/, Then run the following commands

```bash
pytest
```

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Python](https://www.python.org/) - Framework language
* HTML
* CSS

## Authors

* **Ssekitto Ronald** - *Initial work* - [reiosantos](https://github.com/reiosantos)

## Acknowledgments

* Andela Software Development Community
* Inspiration
* Bootcamp 9 team-mates
