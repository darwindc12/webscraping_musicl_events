import requests
import selectorlib


URL = "https://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    request = requests.get(url)
    source = request.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email():
    print("Email was sent")


def store(extracted_local):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read():
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == "__main__":
    result = scrape(URL)
    extracted = extract(result)

    content = read()
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email()


