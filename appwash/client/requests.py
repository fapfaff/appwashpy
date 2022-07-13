from appwash.common.settings import BASE_URL
from appwash.common.enums import HTTP_METHOD
import requests
from typing import TYPE_CHECKING

# Fix cyclical import because of type annotation
if TYPE_CHECKING:
    from appwash import AppWash


class ApiRequest:
    method: HTTP_METHOD = HTTP_METHOD.GET
    url: str
    params: dict
    body: dict
    headers: dict = {
        "platform": "appWash",
        "language": "DE"
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
            self.headers['token'] = client.token

        self.method = str(method)
        self.body = body
        self.url = BASE_URL + endpoint
        self.params = params

        self._perform_request()

    def _perform_request(self):
        response = requests.request(self.method,
                                    url=self.url,
                                    params=self.params,
                                    json=self.body,
                                    headers=self.headers).json()
        self._response = response

    @property
    def response(self):
        return self._response
