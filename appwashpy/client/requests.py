import requests
from appwashpy.common.settings import BASE_URL
from appwashpy.common.enums import HTTP_METHOD
from typing import TYPE_CHECKING

# Fix cyclical import because of type annotation
if TYPE_CHECKING:
    from appwashpy.client.appwash import AppWash


class ApiRequest:
    method: HTTP_METHOD = HTTP_METHOD.GET
    url: str
    params: dict
    body: dict
    headers: dict = {
        "platform": "appWash",
        "language": "EN",
        "Accept": "application/json"
    }
    _response: dict

    def __init__(self,
                 client: "AppWash",
                 endpoint: str,
                 method: HTTP_METHOD = HTTP_METHOD.GET,
                 body: dict = None,
                 params: dict = None,
                 ):

        if endpoint != "/login":
            if client.token == None:
                client.authenticate()
            self.headers['token'] = client.token

        self.method = str(method)
        self.body = body
        self.url = BASE_URL + endpoint
        self.params = params

        self._perform_request()

    def _perform_request(self) -> None:
        self._response = requests.request(self.method,
                                          url=self.url,
                                          params=self.params,
                                          json=self.body,
                                          headers=self.headers).json()

    @property
    def response(self) -> dict:
        return self._response
