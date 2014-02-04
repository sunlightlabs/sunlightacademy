# Sunlight Academy

Sunlight Foundation's training and webinar platform.

## Installation

1. Install dependecies.

        pip install -r requirements.txt

1. Create environment file and set required values. DATABASE_URL should be in the Heroku format expected by [dj-database-url](https://pypi.python.org/pypi/dj-database-url/).

        cp env.example .env

1. Create database and tables. When prompted, create a superuser account.
    
        python manage.py syncdb
        python manage.py migrate

1. Run it. We highly recommend using [foreman](http://rubygems.org/gems/foreman).
    
        foreman start
    

