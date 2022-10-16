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

    def req_body(self, page=None, per_page=None, query=None, filters=None, location=None, distance=None, start_date=None, end_date=None, elite=False):
        return {"page": page, "per_page": per_page, "query": query, "filters": filters, "location": location, "distance": distance, "start_date": start_date, "end_date": end_date, "elite": elite}, None


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


class CoursesEndpoint(BaseEndpoint):
    endpoint = "courses"

    def req_body(self, page=None, per_page=None, category_id=None, name=None, country_id=None, region_id=None, start_date=None, end_date=None, language=None, order=None, course_id=None):
        return {"page": page, "per_page": per_page, "category_id": category_id, "name": name, "country_id": country_id, "region_id": region_id, "start_date": start_date, "end_date": end_date, "language": language, "order": order, "course_id": course_id}, None

class CoursesInfoEndpoint(CoursesEndpoint):
    def resolve_url(self, **kwargs):
        return f"{self.url}/{kwargs['course_id']}"
    
    def req_body(self, course_id=None):
        return None, None
    
class CoursesCategoriesEndpoint(CoursesEndpoint):
    
    def resolve_url(self, **kwargs):
        return f"{self.url}/categories"
    
    def req_body(self,cat_parent_id=None, child_categories=False ):
        return {"cat_parent_id": cat_parent_id, "child_categories":child_categories}, None
    
class SearchAPI:
    def __init__(self, token) -> None:
        self.token = token

    def athletes(self, query, **kwargs):
        return AtheletesSearchEndpoint(self.token, query=query, **kwargs).request()

    def events(self, query, **kwargs):
        return EventsSearchEndpoint(self.token, query=query, **kwargs).request()

    def federations(self, query, **kwargs):
        return FederationsSearchEndpoint(self.token, query=query, **kwargs).request()

    def courses(self, query, **kwargs):
        return CoursesSearchEndpoint(self.token, query=query, **kwargs).request()

    def news(self, query, **kwargs):
        return NewsSearchEndpoint(self.token, query=query, **kwargs).request()

    def videos(self, query, **kwargs):
        return VideosSearchEndpoint(self.token, query=query, **kwargs).request()

class CoursesAPI:
    def __init__(self, token) -> None:
        self.token = token
        
    def search(self, **kwargs):
        return CoursesEndpoint(self.token, **kwargs).request()
    
    def info(self, course_id):
        return CoursesInfoEndpoint(self.token, course_id=course_id).request()
    
    def categories(self, **kwargs):
        return CoursesCategoriesEndpoint(self.token, **kwargs).request()
class TriathlonAPI:
    def __init__(self, token) -> None:
        self.token = token
        self.search = SearchAPI(token)
        self.courses = CoursesAPI(token)
    

if __name__ == "__main__":
    with open("../token.txt", "r", encoding="utf-8") as f:
        token = f.read()
    api = TriathlonAPI(token)
    print(api.courses.info(78443))
