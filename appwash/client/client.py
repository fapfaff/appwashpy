from appwash.client.requests import ApiRequest
from appwash.common.enums import HTTP_METHOD
from appwash.common.helper import current_timestamp


class AppWash:

    email: str
    password: str
    _token_expiry: int = None

    location_id: str = None

    def __init__(self, email: str, password: str, location_id: str = None):
        self.email = email
        self.password = password

        if location_id != None:
            self.location_id = location_id

        self._authenticate()

    def _authenticate(self):
        request = ApiRequest(
            self,
            endpoint='/login',
            method=HTTP_METHOD.POST,
            body={
                "email": self.email,
                "password": self.password
            }
        )

        self._token = request.response['login']['token']
        self._token_expiry = request.response['token_expire_ts']

    @property
    def token(self):
        # Obtain new token if old one is expired
        if(self._token_expiry > current_timestamp()):
            return self._token
        else:
            self._authenticate()
            return self._token
