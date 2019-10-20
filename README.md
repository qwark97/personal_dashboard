# Personal Dashboard

It is backend side of simple web app. It's an app for daily tasks. User is able to post notes, add friends from the outside the app and asign to them all his/her payables and receivables. With Google Search API (implementing in progress) it is also great option for home page in user's browser. 

## Getting Started

### Prerequisites

To run this app you need two things:

1) Python 3.6+

    [Get it here](https://www.python.org/)

2) PostgreSQL

    [Get it here](http://www.postgresqltutorial.com/install-postgresql/)

### Installing

If you already have above you should do following steps:

- Recommended - create virtual environment

```
pip install virtualenv
```
```
cd path/to/project/directory
```
```
virtualenv venv -p python3
```
UNIX
```
venv/bin/activate
```
WINDOWS
```
venv/bin/activate
```

Now you should have your virtual environment active. From now on all following packages will be installed in this particular environment. 

- Now install all packages from requirement.txt
```
pip install -r "requirements.txt"
```

- Database stuff
  1) Create server. You can find how to do this [here](http://www.postgresqltutorial.com/install-postgresql/).
  2) Create database. To do this in SQL Shell run:
  ```
  CREATE DATABASE dashboard;
  ```
  3) Now you have to change 8th line in config.py file. It should look like this:
  ```
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/dashboard'
  ```  
    If you have problems try to find answer [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)
     
  4) Creating models: run following commands:
    ```
    python
    ```
    ```
    from models import db
    ```
    ```
    db.create_all()
    ```
    ```
    exit()
    ```
- Run project:
    ```
    python app.py
    ```
    
Now basic HTML view should be available on http://127.0.0.1:5000/

## Built With

* [Flask](http://flask.pocoo.org/) - a microframework for Python.
* [SQLAlchemy](https://www.sqlalchemy.org/) - the Python SQL Toolkit and Object Relational Mapper.
* [Jinja2](http://jinja.pocoo.org/docs/2.10/) - templating language for Python.
* [darksky](https://darksky.net/dev) and [geocoder](https://pypi.org/project/geocoder/) for weather feature. <br>
And few others around

