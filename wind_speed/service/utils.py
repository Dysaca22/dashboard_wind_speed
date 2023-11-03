from urllib.request import urlopen
import json


def read_json(url):
    with urlopen(url) as response:
        result_ = json.load(response)
    return result_