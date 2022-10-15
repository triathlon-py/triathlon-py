from requests import Request, Session


class TriathlonAPIBaseException(Exception):
    """Base exception for all Triathlon API exceptions."""

    pass


class TriathlonAPIException(TriathlonAPIBaseException):
    """Exception for Triathlon API errors."""

    pass


class TriathlonAPIHTTPException(TriathlonAPIBaseException):
    """Exception for Triathlon API HTTP errors."""

    pass


class TriathlonAPIRateLimitException(TriathlonAPIBaseException):
    """Exception for Triathlon API rate limit errors."""

    pass


class TriathlonAPIAuthenticationException(TriathlonAPIBaseException):
    """Exception for Triathlon API authentication errors."""

    pass


class TriathlonAPIAuthorizationException(TriathlonAPIBaseException):
    """Exception for Triathlon API authorization errors."""

    pass


class TriathlonAPIRequestException(TriathlonAPIBaseException):
    """Exception for Triathlon API request errors."""

    pass


class BaseEndpoint:
    base_url = "https://api.triathlon.org"
    version = "v1"
    endpoint = ""
    method = "GET"
    req = None

    def __init__(self, token, **kwargs) -> None:
        self.url = f"{self.base_url}/{self.version}/{self.endpoint}"
        self.token = token

        send_params, send_data = self.req_body(**kwargs)
        self.session = Session()
        self.headers = {
            "accept": "application/json",
            "apikey": token
        }
        self.req = Request(
            self.method,
            self.resolve_url(**kwargs),
            headers=self.headers,
            params=send_params,
            data=send_data,
        )
        self.prepped = self.req.prepare()

    def resolve_url(self, **kwargs):
        return self.url

    def req_body(self, **kwargs):
        #      get   post
        return None, None

    def parse(self, data):
        return data

    def request(self):
        req = self.session.send(self.prepped)

        if req.status_code == 429:
            raise TriathlonAPIRateLimitException()
        else:
            req.raise_for_status()
            return self.parse(req.json())


class SearchEndpoint(BaseEndpoint):
    endpoint = "search"
    collection = ""

    def resolve_url(self, **kwargs):
        return f"{self.url}/{self.collection}"

    def req_body(self, **kwargs):
        return {"query": kwargs["query"]}, None


class AtheletesSearchEndpoint(SearchEndpoint):
    collection = "athletes"


class EventsSearchEndpoint(SearchEndpoint):
    collection = "events"


class CoursesSearchEndpoint(SearchEndpoint):
    collection = "courses"


class FederationsSearchEndpoint(SearchEndpoint):
    collection = "federations"


class NewsSearchEndpoint(SearchEndpoint):
    collection = "news"


class VideosSearchEndpoint(SearchEndpoint):
    collection = "videos"


class AthleteEndpoint(BaseEndpoint):
    endpoint = "athlete"


class TriathlonAPI:
    def __init__(self, token) -> None:
        self.token = token

    def search_athletes(self, query):
        return AtheletesSearchEndpoint(self.token, query=query).request()
