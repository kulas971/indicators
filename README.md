![HomePageSS1](/indicators.png)

# Indicators Web App
Indicators is a simple web application that takes financial statements in .xml files that you can download at [https://ekrs.ms.gov.pl/rdf/pd/search_df](https://ekrs.ms.gov.pl/rdf/pd/search_df) and returns specific indicators (based on provided statements) in the table as output.
Xml files come in encrypted so Indicators uses 3rd party web app [https://e-sprawozdania.biz.pl/show/](https://e-sprawozdania.biz.pl/show/) for decoding purposes. 
An idea for this app came to me in my previous job, where we had to do this manually, and in order to save time I came up with this app.

Uploading files is allowed only for registered users. 

Biggest challenges:
- Parsing the documents - content of the reports differs sometimes (number of tables, number of rows in tables, names of cells or even special characters within strings).
- Passing data from one view to another - I didn't want to pass the data through the database, because I wasn't sure about legal part of storing the data like that. Instead, I used request.session

To do:
- Upgrade the parser so it works for all types of reports (for now it works for standard and consolidated financial raports)

# How to use
Download the repository.
Start with docker:
cd to /indicators and use docker-compose
```
docker-compose up
```
Start with Python:
Preferably create a virtual environment.
cd to /indicators/indicatorsproject
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.
```
pip install -r requirements.txt
```
With requirements installed you can run the app:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
# Samples
In /indicators/samples you can find financial statements of real companies that have been anonymized
