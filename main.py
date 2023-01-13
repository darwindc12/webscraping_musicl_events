import ssl
import time
import requests
import selectorlib
import smtplib


URL = "https://programmer100.pythonanywhere.com/tours/"


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
    with open("data.txt", "a") as file:
        file.write(extracted_local + "\n")


def read():
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == "__main__":
    while True:
        result = scrape(URL)
        extracted = extract(result)
        print(extracted)

        content = read()
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="Hey! new event was found")
        time.sleep(1)

