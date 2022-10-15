class URL:
    base_url = "https://api.triathlon.org"
    version = "v1"
    def __init__(self, endpoint, query=None) -> None:
        if query:
            self.url = f"{self.base_url}/{self.version}/{endpoint}?query={query}"
        else:
            self.url = f"{self.base_url}/{self.version}/{endpoint}"