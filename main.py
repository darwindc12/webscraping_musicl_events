import ssl
import time
import requests
import selectorlib
import smtplib
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"


class Event:
    def scrape(self, url):
        request = requests.get(url)
        source = request.text
        return source


    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value

class Email:
    def send_email(self, message):
        host = 'smtp.gmail.com'
        port = 465

        username = "cpythonista@gmail.com"
        password = "rpoqtvgivcxsgavw"

        receiver = "cpythonista@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)
        print("Email was sent")

class Database:

    def __init__(self, filepath):
        self.connection = sqlite3.connect(filepath)

    def store(self, extracted_local):
        row = extracted_local.split(",")
        row = [word.strip() for word in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO event values(?,?,?)", row)
        self.connection.commit()


    def read(self, extracted_local):
        row = extracted_local.split(",")
        row = [word.strip() for word in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM event WHERE band=? AND city = ? AND date = ?", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        result = event.scrape(URL)
        extracted = event.extract(result)
        print(extracted)
        if extracted != "No upcoming tours":
            database = Database(filepath="data.db")
            rows = database.read(extracted)
            if not rows:
                database.store(extracted)
                email = Email()
                email.send_email(message="Hey! new event was found")
        time.sleep(1)

