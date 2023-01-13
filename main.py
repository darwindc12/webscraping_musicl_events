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


if __name__ == "__main__":
    result = scrape(URL)
    # print(result)
    extracted = extract(result)
    print(extracted)
