import ssl
import time
import requests
import selectorlib
import smtplib
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

def scrape(url):
    request = requests.get(url)
    source = request.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
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


def store(extracted_local):
    row = extracted_local.split(",")
    row = [word.strip() for word in row]
    cursor.execute("INSERT INTO event values(?,?,?)", row)
    connection.commit()


def read(extracted_local):
    row = extracted_local.split(",")
    row = [word.strip() for word in row]
    band, city, date = row
    cursor.execute("SELECT * FROM event WHERE band=? AND city = ? AND date = ?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    while True:
        result = scrape(URL)
        extracted = extract(result)
        print(extracted)
        if extracted != "No upcoming tours":
            rows = read(extracted)
            if not rows:
                store(extracted)
                send_email(message="Hey! new event was found")
        time.sleep(1)

