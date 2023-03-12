# gym-workout-API

How to install dependencies (assuming pip is installed):
  - run: pip install -r requirements.txt

Used database: SQLAlchemy (1.4.46) => SQLite

How to initialize database:
  - run: flask init_db

How to test database:
  - run: flask test_db

How to run tests:

Windows based system:
  - set FLASK_APP=gymworkoutapi
  - set FLASK_DEBUG=1
  - pytest --cov=gymworkoutapi
  OPTIONAL (get html coverage report as output):
  - pytest --cov=gymworkoutapi --cov-report html

Linux based system:
  - EXPORT FLASK_APP=gymworkoutapi
  - EXPORT FLASK_DEBUG=1
  - pytest --cov=gymworkoutapi
  OPTIONAL (get html coverage report as output):
  - pytest --cov=gymworkoutapi --cov-report html

Git bash etc:
  - export FLASK_APP=gymworkoutapi
  - export FLASK_DEBUG=1
  - pytest --cov=gymworkoutapi
  OPTIONAL (get html coverage report as output):
  - pytest --cov=gymworkoutapi --cov-report html

Check code quality (pylint):
  - pylint gymworkoutapi --disable=no-member,import-outside-toplevel,no-self-use
