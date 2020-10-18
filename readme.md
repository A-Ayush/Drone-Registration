# Flask-Intro with structured format

*You can refer to Flask’s documentation.
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)*

## Requirements file consists the following:

-bcrypt==3.1.7
-cffi==1.14.0
-click==7.1.1
-Flask==1.1.2
-Flask-Bcrypt==0.7.1
-Flask-Login==0.5.0
-Flask-SQLAlchemy==2.4.1
-Flask-WTF==0.14.3
-itsdangerous==1.1.0
-Jinja2==2.11.2
-MarkupSafe==1.1.1
-pycparser==2.20
-six==1.14.0
-SQLAlchemy==1.3.16
-Werkzeug==1.0.1
-WTForms==2.2.1
-Gunicorn=20.1

## Installation

**Creating Virtual Environment**

You can create a virtual environment and install the required packages with the following commands:

$ virtualenv venv
$ . venv/bin/activate
(venv) $ **your source file**

or 
On linux system,
$ python3 -m venv <env_name>
To activate the env just type in terminal,
$ source <env_name>/bin/activate

- install all the dependencies as mentioned in **Reqirements**
$ python3 <env_name>/bin/activate
$ pip install -r <requirements.txt> file
## Running Command

With the virtual environment activated you can cd into any of the examples and run the main script.

(venv) $ python mypage.py
or 
(venv) $ export FLASK_APP=<file_name.py>
(venv) $ flask run

