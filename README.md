# gym workout API

DEADLINE 2 (database):

External libraries:
  - flask
  - flask-sqlalchemy

How to install dependencies (assuming pip is installed):
  - run: pip install -r requirements.txt

Used database: SQLAlchemy (1.4.46) => SQLite

How to run tests:

Windows based system:
  - set FLASK_APP=gymworkoutapi
  - set FLASK_DEBUG=1
  - pytest --cov=gymworkoutapi

Linux based system:
  - EXPORT FLASK_APP=gymworkoutapi
  - EXPORT FLASK_DEBUG=1
  - pytest --cov=gymworkoutapi
