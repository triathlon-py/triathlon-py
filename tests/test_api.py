import os

def get_token():
    return os.environ["TRIATHLON_API_TOKEN"]    

from triathlon import TriathlonAPI

def test_setup():
    api = TriathlonAPI(get_token())