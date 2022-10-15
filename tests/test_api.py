
def get_token():
    with open("token.txt", r") as token:
        return token.read()

from triathlon import TriathlonAPI

def test_setup():
    api = TriathlonAPI(get_token())
