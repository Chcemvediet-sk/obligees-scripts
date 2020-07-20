import re
from difflib import ndiff

import requests
import requests_cache

BASE_URL = "https://api.posta.sk/private/search"


def norm_query(query: str):
    return re.sub(r"^č.\s", "", query)


def num_diffs(a, b):
    """
    Get number of differences between two strings
    """
    return sum([i[0] != ' ' for i in ndiff(a, b)]) / 2


def get_official_zip(query):
    """
    Get official ZIP code from Slovak post API
    Note: Cached requests
    """
    requests_cache.install_cache("zip_cache", backend="sqlite", expire_after=None)
    response = requests.get(BASE_URL, params={"q": norm_query(query), "m": 'zip'})
    print(norm_query(query))
    if response.status_code == requests.codes.ok:
        data = response.json()
        print(data)
        return ",".join([address['zip'] for address in data['addresses']])


def norm_zip(zipcode):
    """
    Normalize ZIP codes - strip whitespaces
    """
    print(zipcode)
    print(type(zipcode))
    return re.sub(r"\s*", "", zipcode)


def diff_severity(zip1, zip2):
    """
    Calculate severity of zip codes difference
        - right digits are less important (probably geographically closer)
    """
    norm_zip1 = norm_zip(zip1)
    norm_zip2 = norm_zip(zip2)
    abs_value = abs(int(norm_zip2)-int(norm_zip1))

    diff_char = num_diffs(norm_zip1, norm_zip2)
    if 0 < diff_char <= 2 and abs_value < 100:
        return "WARNING"
    elif 2 < diff_char <= 3 and abs_value < 1000:
        return "ERROR"
    else:
        return "FATAL"


def zip_equals(zip1, zip2):
    return norm_zip(zip1) == norm_zip(zip2)
