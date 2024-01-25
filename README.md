# StockSmart.CoreAPIs
Backend Server implemented in Django connects to Postgres Database, Utilises Redis for Caching.
Stock Smart, an emerging platform, leverages cutting-edge Artificial Intelligence to deliver institutional-grade investing and trading data, empowering retail investors with advanced algorithms for trend identification, social sentiment analysis, and informed financial decision-making.

### Spinning the Server

`python manage.py runserver`

## Creating virtual env for the project

`python -m venv venv`

Activate the Virtualenv and
Install the requirements using

` pip install -r requirements.txt`

### Attach pre-commit to project using the following command

`pre-commit install`

### Commands to run migrations of Database (LOCAL SETUP)

`python manage.py makemigrations `

`python manage.py migrate`

### Creating a Super User

`python manage.py createsuperuser`

### Creates a set of Users

`python manage.py create_users`

### Loads Stock data

`python manage.py load_stocks`

### Loads Industries for Stocks data

Should be executed only after load_stocks command

`python manage.py load_industries`

### Loads Smallcases data

`python manage.py load_smallcases`

### Update Smallcases data

`python manage.py update_smallcases`

### Load Calendar Events data

`python manage.py load_calendar_events`

### Create Watchlists for Prev Created Users

`python manage.py create_watchlists`


### To Check "Black" formatting changes
`black --check ./`
