# Event Scraper
This Python code scrapes data from a website and sends an email when a new event is found. It also stores the event data in a SQLite database.

## Installation
This code requires the following packages to be installed:

* requests
* selectorlib
* smtplib
* sqlite3

## Usage
To use this code, run the script event_scraper.py. The script will scrape the website at the specified URL and extract the event data. If a new event is found, it will be stored in the database and an email will be sent.

The email account used for sending the email is hardcoded in the code. You will need to modify the code to use your own email account.

The database file path is also hardcoded in the code. You will need to modify the code to use your own database file path.
