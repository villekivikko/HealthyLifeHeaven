# gym-workout-API

How to install dependencies (assuming pip is installed):
  - run: pip install -r requirements.txt

Used database: SQLAlchemy (1.4.46) => SQLite

Set the Flask app and debug variable correctly:
  - Windows based system:
    - set FLASK_APP=gymworkoutapi
    - set FLASK_DEBUG=1
  - Linux based system:
    - EXPORT FLASK_APP=gymworkoutapi
    - EXPORT FLASK_DEBUG=1
  - Git bash etc:
    - export FLASK_APP=gymworkoutapi
    - export FLASK_DEBUG=1

How to initialize database:
  - run: flask init_db

How to test database:
  - run: flask test_db

How to run tests:
  - pytest --cov=gymworkoutapi
  - OPTIONAL (get html coverage report as output): pytest --cov=gymworkoutapi --cov-report html

Check code quality (pylint):
  - pylint gymworkoutapi --disable=no-member,import-outside-toplevel,no-self-use

Test documentation with Swagger: 
- flask run
- on your browser go to: localhost:5000/apidocs/
