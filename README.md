# Adverity

Option B. - Django solution

## The Solution

I tried to create a very simple solution, what fulfill the requirements. 
Originally I wanted to separate the ETL from the rest of the application, 
but we have only one data source atm, so I decided to do put everything under one app.

I played around with several ETL tools, i felt them overkill so I choose to create my own 
lightweight solution and wrote a management command to load the data. 

For the frontend I had to use Django views, so instead of create an api (what I would prefer to use), 
I generated the data directly into the view.

To show the charts, I'm using Highcharts, because I never used it before and it looks fancy :)

## Locally
Setup the environment:
```
pip install -r requirements
python manage.py migrate
python manage.py collectstatic
```
To load the data:
```
python manage.py import_data
```
Run the server:
```
python manage.py runserver
```

## Docker

Setup and run the environment:
```
make build
make up
```

Load the data:
```
make importdata
```

## TODOs and suggested improvement:

* The ETL strategy is far from production ready, need error handling insert chunks etc...
* If we want to trigger the file load from the UI, we need celery to do the load in the background.
* When I have limited amount of time I use UnitTest, but PyTest would be more modern.
* Test the templates
* Maybe use Django Forms at the select
* With a different UI, we could first select Source and prefilter campagins to show only the ones 
what has available data for the selected source(s).
* Add Sentry
* Add logging specially