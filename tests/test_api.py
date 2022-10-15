def get_token():
    with open("token.txt", "r", encoding="utf-8") as f:
        return f.read()

from triathlon import TriathlonAPI

def test_setup():
    api = TriathlonAPI(get_token())