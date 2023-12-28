# StockSmart.CoreAPI
Backend Server implemented in Django connects to Postgres Database, Utilises Redis for Caching.
Stock Smart, an emerging platform, leverages cutting-edge Artificial Intelligence to deliver institutional-grade investing and trading data, empowering retail investors with advanced algorithms for trend identification, social sentiment analysis, and informed financial decision-making.

## Spinning the Server
```python manage.py runserver```


# Setting up the project
## Cloning the repo
```git clone https://github.com/KrishnaManohar1997/StockSmart.CoreAPI.git```


## Creating virtual env for the project
```python -m venv .venv```

Install the requirements using ``` pip install -r requirements.txt```

## Attach pre-commit to project using the following command

```pre-commit install```

# Database Related Operations
## Migrations
Generate the migration files

```python manage.py makemigrations```


Migrate the schema to Database

```python manage.py migrate```
